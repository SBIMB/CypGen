import os
import sys
import subprocess
from snv_def_modules import *
from sv_modules import *

print("--------------------------------------------\n")

print("CYP2D6 Star Allele Calling with CypGen\n")

print("--------------------------------------------\n")



database = sys.argv[1]
infile = sys.argv[2]
infile_full = sys.argv[3]
infile_full_gt = sys.argv[4]
infile_spec = sys.argv[5]
sv_del = sys.argv[6]
sv_dup = sys.argv[7]
# core_var_sum = sys.argv[8]
cov_file = sys.argv[8]
hap_dbs = sys.argv[9]

#cn = get_total_CN(cov_file)


cn = get_total_CN(cov_file)[0]

print("Initially computed CN = {}".format(cn))

supp_core_vars = get_core_variants(infile, cn)

print("\nSample core variants:")
print(supp_core_vars)


snv_def_calls = cand_snv_allele_calling(database, infile, infile_full, infile_full_gt, infile_spec, cn)

if snv_def_calls == None:
    print("\nResult:")
    print("Possible novel allele or suballele present: interpret with caution")
    sys.exit()

snv_cand_alleles = snv_def_calls[0]

print("\nCandidate alleles:")
print(snv_cand_alleles)


snv_def_alleles = snv_def_calls[-1]

dip_variants = get_all_vars_gt(infile_full_gt)


print("\nResult:")


# cn = get_total_CN(cov_file)[0]
av_cov = get_total_CN(cov_file)[3]
cn_in1_3pr = get_total_CN(cov_file)[2]
cn_ex9_3pr = get_total_CN(cov_file)[4]
in1_3pr_float = get_total_CN(cov_file)[5]

cov_in4_3pr = get_total_CN(cov_file)[6]
cov_5pr_in4 = get_total_CN(cov_file)[7]
cn_2d7_ex9 = get_total_CN(cov_file)[8]
cn_2d7_in4_in8 = get_total_CN(cov_file)[9]




if snv_def_alleles != '*2/*2':
    in_list = dup_test_init(sv_dup, av_cov)



if cn == '2' and snv_def_alleles == '*4/*4':
    
    test_68 = hyb_test_5_68_4(sv_del, in1_3pr_float, av_cov)

    if test_68 == 'norm_art':
        pass
    elif test_68 == 'del_hyb':
        snv_def_alleles = (snv_def_alleles.replace('*4', '*5', 1)).replace('*4', '*68+*4')

    print("\n" + snv_def_alleles)



elif cn == '2':
    if 'or' in snv_def_alleles:
        print ("\n")
        print (snv_def_alleles)
    else:
        snv_def_alleles = snv_def_alleles.split("/")

        if snv_def_alleles[0] == '*2' or snv_def_alleles[1] == '*2':
            ind_star2 = snv_def_alleles.index('*2')
            ind_other = 1 - ind_star2

            test_13_v2 = hybrid_13_test1(cov_in4_3pr, cov_5pr_in4)

            if test_13_v2 == 'norm_var':
                print("\n")
                print("/".join(snv_def_alleles))

            elif test_13_v2 == 'hyb_13_2':
                print("\n")
                print(snv_def_alleles[ind_other] + "/" + "*13+*2")

        else:
            print("\n")
            print("/".join(snv_def_alleles))


elif cn == '0':
    del_confirm = del_test(sv_del)
    if del_confirm == '*5/*5':
        print ("\n" + del_confirm)

    elif del_confirm == '*5':
        print ("\n" + del_confirm + "/" + "*other")

    else:
        print ("*5/*5")
        
elif cn == '1':
    del_confirm = del_test(sv_del)
 
    if "or" in snv_def_alleles and del_confirm == None:
        print ("\n")
        print (snv_def_alleles + "\t" + "Possible CYP2D6 gene deletion (*5) present")

    elif "or" not in snv_def_alleles and del_confirm == None:
        snv_def_alleles = snv_def_alleles.split("/")
        snv_cand_alleles = snv_cand_alleles.split("_")

        if snv_def_alleles[0] == snv_def_alleles[1]:
            print ("\n")
            print (snv_def_alleles[0] + "/" + "*5")

        elif snv_def_alleles[0] != snv_def_alleles[1]:
            samp_allele1 = del_adv_test(hap_dbs, snv_cand_alleles[0], snv_cand_alleles[1], snv_def_alleles[0], snv_def_alleles[1], supp_core_vars)
            # print(samp_allele1)                                                                                                                         
            print ("\n")
            print (samp_allele1 + "/" + "*5")

    else:
        snv_def_alleles = snv_def_alleles.split("/")
        snv_cand_alleles = snv_cand_alleles.split("_")

        if snv_def_alleles[0] == snv_def_alleles[1]:
            print ("\n")
            if del_confirm == "*5/*5":
                del_confirm = "*5"
            print (del_confirm + "/" + snv_def_alleles[0])

        elif snv_def_alleles[0] != snv_def_alleles[1]:
            samp_allele1 = del_adv_test(hap_dbs, snv_cand_alleles[0], snv_cand_alleles[1], snv_def_alleles[0], snv_def_alleles[1], supp_core_vars)
            print ("\n")
            if del_confirm == "*5/*5":
                del_confirm = "*5"
            print (del_confirm + "/" + samp_allele1)


elif (int(cn) == 3 or int(cn) == 4) and snv_def_alleles != None:

    # in_list = dup_test_init(sv_dup, av_cov)
    # print (snv_def_alleles)
    # print (snv_cand_alleles)
    orig = snv_def_alleles

    if "or" in snv_def_alleles:
        print ("\n" + snv_def_alleles + "\t" + "Duplication present")

    else:
        snv_def_alleles = snv_def_alleles.split("/") 
        snv_cand_alleles = snv_cand_alleles.split("_")


        if snv_def_alleles[0] == '*90' or snv_def_alleles[1] == '*90':
            
            alt_allele_ind = 1 - snv_def_alleles.index('*90')
            alt_allele = snv_def_alleles[alt_allele_ind]
            sp_allele = tandem_90_1(in_list, alt_allele, cn)
            

            sp_allele1 = sp_allele.split("/")


            if "*10x2" in sp_allele1:

                test_36 = hybrid_test_36(sv_dup, cn, av_cov, cn_ex9_3pr, cn_2d7_ex9, cn_2d7_in4_in8)

                if test_36 == 'norm_dup':
                    pass

                elif test_36 == 'hyb_36_10':
                    sp_allele = sp_allele.replace('*10x2', '*36+*10')

                elif test_36 == 'hyb_36_36':
                    sp_allele = sp_allele.replace('*10x2', '*36x2')

            print(sp_allele)

        
        elif snv_def_alleles[0] != snv_def_alleles[1]:
            #print("\n" + dup_test(sv_dup, hap_dbs, snv_def_alleles[0], snv_def_alleles[1], cn))
            #print (snv_cand_alleles)
            print ("\n")
            phased_dup = dup_test_cn_3_4(sv_dup, hap_dbs, snv_cand_alleles[0], snv_cand_alleles[1], snv_def_alleles[0], snv_def_alleles[1], cn, av_cov, in_list)

           # print (phased_dup)
            
            phased_dup1 = phased_dup.split("/")

            # print (hybrid_test_68(sv_dup, cn, av_cov, cn_in1_3pr, in_list))

            if '*4x2' in phased_dup1:
                count1 = phased_dup1.count('*4x2')
                a_ind1 = phased_dup1.index('*4x2')
                a_ind2 = 1 - a_ind1
                other_hap = phased_dup1[a_ind2]

                if count1 == 1:

                    test_68 = hybrid_test_68(sv_dup, cn, av_cov, cn_in1_3pr, in_list)
                    

                    if test_68 == 'norm_dup':
                        pass
                    elif test_68 == 'hyb_68':
                        if int(cn_in1_3pr) < int(cn):
                            phased_dup = phased_dup.replace('*4x2', '*68+*4')

                        elif int(cn_in1_3pr) == int(cn) and 'x' not in other_hap:
                            phased_dup = phased_dup.replace('*4x2', '*68+*4')
                            phased_dup = phased_dup.replace(other_hap, (other_hap + 'x2'))

                elif count1 == 2:
                    pass

            if '*10x2' in phased_dup1:
                count2 = phased_dup1.count('*10x2')
                b_ind1 = phased_dup1.index('*10x2')
                b_ind2 = 1 - b_ind1


                if count2 == 1:
                    test_36 = hybrid_test_36(sv_dup, cn, av_cov, cn_ex9_3pr)
                    # print (test_36)

                    if test_36 == 'norm_dup':
                        pass

                    elif test_36 == 'hyb_36_10':
                        phased_dup = phased_dup.replace('*10x2', '*36+*10')

                    elif test_36 == 'hyb_36_36':
                        phased_dup = phased_dup.replace('*10x2', '*36x2')


            if '*10x3' in phased_dup1:
                count3 = phased_dup1.count('*10x3')
                c_ind1 = phased_dup1.index('*10x3')
                c_ind2 = 1 - c_ind1

                if count3 == 1:
                    test_36 = hybrid_test_36_mod(sv_dup, cn, av_cov, cn_ex9_3pr)
                   # print (test_36)

                    if test_36 == 'norm_mt':
                        pass

                    elif test_36 == 'hyb_36_10': 
                        phased_dup = phased_dup.replace('*10x3', '*36+*10x2')

                    # elif test_36 == 'hyb_36_10' and phased_dup1[c_ind2] == '*10':                                                                          

                    elif test_36 == 'hyb_36_36':
                        phased_dup = phased_dup.replace('*10x3', '*36x2+*10')

            print(phased_dup)


        elif snv_def_alleles[0] == snv_def_alleles[1]:
            
            rt_2 = int(cn) - 1
            print ("\n")
            phased_dup = (snv_def_alleles[0] + "/" + snv_def_alleles[1] + "x" + str(rt_2))

            phased_dup1 = phased_dup.split("/")

            if '*4x2' in phased_dup1:
                count1 = phased_dup1.count('*4x2')
                a_ind1 = phased_dup1.index('*4x2')
                a_ind2 = 1 - a_ind1

            # for i in phased_dup1:
            #     if i != '*4x2':
            #         other_hap = i

                if count1 == 1:
                    test_68 = hybrid_test_68(sv_dup, cn, av_cov, cn_in1_3pr)

                    if test_68 == 'norm_dup':
                        pass

                    elif test_68 == 'hyb_68':
                        phased_dup.replace('*4x2', '*68+*4')


            if '*10x2' in phased_dup1:
                count2 = phased_dup1.count('*10x2')
                b_ind1 = phased_dup1.index('*10x2')
                b_ind2 = 1 - b_ind1

                if count2 == 1:
                    test_36 = hybrid_test_36(sv_dup, cn, av_cov, cn_ex9_3pr)
                   # print (test_36)

                    if test_36 == 'norm_dup':
                        pass

                    elif test_36 == 'hyb_36_10':
                        phased_dup = phased_dup.replace('*10x2', '*36+*10')

                    elif test_36 == 'hyb_36_36':
                        phased_dup = phased_dup.replace('*10x2', '*36x2')

            if '*10x3' in phased_dup1:
                count3 = phased_dup1.count('*10x3')
                c_ind1 = phased_dup1.index('*10x3')
                c_ind2 = 1 - c_ind1
                
                if count3 == 1:
                    test_36 = hybrid_test_36_mod(sv_dup, cn, av_cov, cn_ex9_3pr)
                    
                   # print (test_36)
                    
                    if test_36 == 'norm_mt':
                        pass
                    
                    elif test_36 == 'hyb_36_10':
                        phased_dup = phased_dup.replace('*10x3', '*36+*10x2')

                    # *10x2/*36+*10
                    
                    elif test_36 == 'hyb_36_36':
                        phased_dup = phased_dup.replace('*10x3', '*36+*10').replace('*10', '*36+*10')                

            print(phased_dup)




elif int(cn) > 4 and snv_def_alleles != None:

    if "or" in snv_def_alleles:
        print ("\n" + snv_def_alleles + "\t" + "Duplication present")

    else:
        snv_def_alleles = snv_def_alleles.split("/")
        snv_cand_alleles = snv_cand_alleles.split("_")

        phased_dup = dup_test_cn_n(sv_dup, hap_dbs, snv_cand_alleles[0], snv_cand_alleles[1], snv_def_alleles[0], snv_def_alleles[1], cn, av_cov, in_list)

        print(phased_dup)



elif int(cn) > 2 and snv_def_alleles == None:
    
    print("Possible rare CYP2D6/2D7 hybrid present")
