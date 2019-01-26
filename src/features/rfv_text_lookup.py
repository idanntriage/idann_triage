# Code based on /modeling/cdc_model_processing.py
# Author: Roseanna Hopper

#Recoding all RFV codes to text
def RFVtext(i):
    if i==10050:
        return 'chills'
    if i==10100:
        return 'fever high temperature'
    if i==10120:
        return 'other symptoms of body temperature'
    if i==10121:
        return 'feeling cold'
    if i==10122:
        return 'feeling hot'
    if i==10123:
        return 'feeling hot and cold'
    if i==10150:
        return 'tiredness exhaustion exercise intolerance fatigue lack of energy  no energy run down worn out'
    if i==10200:
        return 'general weakness'
    if i==10250:
        return 'general ill feeling diffuse cx feeling bad all over illness nos malaise not feeling well multiple complaints sick nos'
    if i==10300:
        return 'fainting (syncope) blacking out fainting spells passing out'
    if i==10350:
        return 'symptoms of fluid abnormalities fluid imbalance fluid retention holding water'
    if i==10351:
        return 'edema ankles swelling (both) bloated dropsy legs (both) peripheral swollen with water'
    if i==10352:
        return 'excessive sweating perspiration cold sweats diaphoresis'
    if i==10353:
        return 'excessive thirst'
    if i==10400:
        return 'weight gain fat pads (localized) fatty deposits obesity overweight too fat'
    if i==10450:
        return 'weight loss'
    if i==10451:
        return 'recent weight loss'
    if i==10452:
        return 'underweight'
    if i==10460:
        return 'symptoms of the face nec mass'
    if i==15450:
        return 'stomach and abdominal pain cramps and spasms gastric pain'
    if i==15451:
        return 'abdominal pain cramps spasms nos abdominal discomfort no gas pains intestinal colic'
    if i==15452:
        return 'lower abdominal pain cramps spasms right lower quadrant (rlq) pain left lower quadrant (llq) pain inguinal pain'
    if i==15453:
        return 'upper abdominal pain cramps spasms epigastric pain left upper quadrant (luq) pain pain in umbilical region right upper quadrant (ruq) pain'
    if i==15450:
        return 'change in abdominal size'
    if i==15650:
        return 'distention fullness nos abdominal bloating stomach fullness'
    if i==15651:
        return 'mass or tumor mass in groin mass inguinal'
    if i==15652:
        return 'abdominal swelling nos'
    if i==15700:
        return 'appetite abnormal'
    if i==15701:
        return 'excessive appetite eats too much always hungry'
    if i==15702:
        return 'decreased appetite decreased fluid intake loss of appetite not eating not hungry'
    if i==15750:
        return 'difficulty eating'
    if i==15800:
        return 'gastrointestinal bleeding bowel'
    if i==15801:
        return 'blood in stool (melena)'
    if i==15802:
        return 'vomiting blood (hematemisis)'
    if i==15850:
        return 'flatulance bloated gas distention due to gas excessive gas gas'
    if i==15900:
        return 'constipation'
    if i==15950:
        return 'diarrhea loose stools the runs'
    if i==16000:
        return 'other symptoms or changes in bowel function'
    if i==16001:
        return 'dischange in stools guaiac positive hemocult positive mucus pus'
    if i==16002:
        return 'stool worms'
    if i==16003:
        return 'changes in size color shape or odor bulky stools too narrow unusual odor or color'
    if i==16004:
        return 'incontinence of stool dirty pants (encopresis) leaking stools'
    if i==16050:
        return 'symptoms referable to anus-rectum'
    if i==16051:
        return 'pain burning irritation'
    if i==16052:
        return 'anus-rectum bleeding'
    if i==16053:
        return 'anus-rectum swelling or mass'
    if i==16054:
        return 'anus-rectum itching'
    if i==16100:
        return 'symptoms of liver gallbladder and biliary tract'
    if i==16101:
        return 'liver gallbladder and biliary tract pain'
    if i==16102:
        return 'jaundice yellow eyes yellow skin'
    if i==16150:
        return 'other and unspecified symptoms referable to digestive system abdominal pressure bad breath epigastric distress gastrointestinal distress halitosis hiccoughs regurgitation (adult) sour taste in mouth stomach problem stomach trouble'
    if i==16400:
        return 'abnormalities of urine'
    if i==16401:
        return 'blood in urine (hematuria)'
    if i==16402:
        return 'pus in urine'
    if i==16403:
        return 'unusual color or odor'
    if i==16450:
        return 'frequency and urgency of urination'
    if i==16451:
        return 'excessive urination night (nocturia)'
    if i==16500:
        return 'painful urination burning discomfort'
    if i==16550:
        return 'incontinence of urine (enuresis)'
    if i==16551:
        return 'involuntary urination can\'t hold urine dribbling wetting pants'
    if i==16552:
        return 'bedwetting'
    if i==16600:
        return 'other urinary disfunctions trouble going urinary pressure weak stream'
    if i==16601:
        return 'retention of urine can\'t urinate'
    if i==16602:
        return 'hesitancy difficulty in starting stream'
    if i==16603:
        return 'urine large volume polyuria'
    if i==16604:
        return 'urine mall volume'
    if i==16650:
        return 'symptoms of bladder bladder trouble'
    if i==16651:
        return 'bladder pain'
    if i==16652:
        return 'bladder infection'
    if i==16653:
        return 'bladder mass'
    if i==16700:
        return 'symptoms of the kidneys kidney trouble'
    if i==16701:
        return 'kidney pain'
    if i==16702:
        return 'kidney infection'
    if i==16703:
        return 'kidney mass'
    if i==16750:
        return 'urinary tract infection nos genitourinary infection urine infection'
    if i==16800:
        return 'other symptoms referable to urinary tract passed stones urethral bleeding urinary irritation'
    if i==17000:
        return 'symptoms of penis'
    if i==17001:
        return 'penis pain aching soreness tenderness painful erection'
    if i==17002:
        return 'penis infection inflammation swelling'
    if i==17003:
        return 'penis lumps bumps growths warts'
    if i==17050:
        return 'penile discharge'
    if i==17100:
        return 'symptoms of prostate prostate trouble'
    if i==17101:
        return 'prostate swelling'
    if i==17102:
        return 'prostate infection'
    if i==17150:
        return 'symptoms of the scrotum and testes'
    if i==17151:
        return 'scrotum and testes pain aching tenderness'
    if i==17152:
        return 'scrotum and testes swelling inflammation'
    if i==17153:
        return 'scrotum and testes growths warts lumps bumps'
    if i==17154:
        return 'scrotum and testes itching jock itch'
    if i==17200:
        return 'other symptoms of male reproductive system blood in semen early sexual development males painful ejaculation'
    if i==17300:
        return 'absence of menstruation (amenorrhea)'
    if i==17350:
        return 'irregularity of menstrual interval'
    if i==17351:
        return 'menstruation frequent'
    if i==17352:
        return 'menstruation infrequent'
    if i==17353:
        return 'menstruation unpredictable'
    if i==17400:
        return 'irregularity of menstrual flow'
    if i==17401:
        return 'menstruation excessively heavy (menorrhagia)'
    if i==17402:
        return 'menstruation scanty flow (oligomenorrhea)'
    if i==17403:
        return 'abnormal menstrual material including clots'
    if i==17450:
        return 'menstrual symptoms other and unspecified long periods'
    if i==17451:
        return 'premenstrual symptoms pms bloating before periods premenstrual tension or irritability'
    if i==17452:
        return 'painful menstruation (dysmenorrhea) menstrual cramps pain in legs and back during menstruation'
    if i==17500:
        return 'menopause symptoms'
    if i==17501:
        return 'early or late onset of menopause'
    if i==17502:
        return 'vasomotor symptoms - hot flashes'
    if i==17503:
        return 'emotional symptoms change of life problems'
    if i==17550:
        return 'uterine and vaginal bleeding'
    if i==17551:
        return 'intermenstrual bleeding (metrorrhagia) bleeding between periods breakthrough bleeding'
    if i==17552:
        return 'postmenopausal bleeding'
    if i==17553:
        return 'postcoital bleeding female'
    if i==17600:
        return 'vaginal discharge bloody discharge brown discharge white leukorrhea discharge excessive discharge'
    if i==17650:
        return 'other vaginal symptoms'
    if i==17651:
        return 'vaginal pain'
    if i==17652:
        return 'vaginal infection'
    if i==17653:
        return 'vaginal itching burning'
    if i==17653:
        return 'vaginal dryness'
    if i==17700:
        return 'vulvar disorders'
    if i==17701:
        return 'vulvar itching and irritation swelling'
    if i==17702:
        return 'vulvar mass lump'
    if i==17703:
        return 'vulvar growth wart cyst ulcer sore'
    if i==17750:
        return 'pelvic symptoms'
    if i==17751:
        return 'pelvic pain'
    if i==17752:
        return 'pelvic pressure or dropping sensation feeling of uterus falling out'
    if i==17900:
        return 'problems of pregnancy fetal movement'
    if i==17901:
        return 'pain during pregnancy'
    if i==17902:
        return 'spotting bleeding during pregnancy'
    if i==17903:
        return 'symptoms of onset of labor water broke ruptured membranes labor pain contractions labor nos'
    if i==17910:
        return 'postpartum problems bleeding pain'
    if i==17950:
        return 'other symptoms referable to the female reproductive system early sexual development female frequent miscarriage'
    if i==18000:
        return 'pain or soreness of breast tenderness'
    if i==18050:
        return 'lump or mass of breast bump knot nodule cyst'
    if i==18100:
        return 'other symptoms referable to breast'
    if i==18101:
        return 'bleeding or dischange from nipple or breast'
    if i==18102:
        return 'postpartum problems inlcudes engorgement postpartum infection nursing difficulties'
    if i==18103:
        return 'problems with breast shape or size too large too small sagging uneven development'
    if i==18150:
        return 'symptoms of infertility can\'t get pregnant inability to conceive sterility'
    if i==18200:
        return 'hormone deficiency or problem'
    if i==18250:
        return 'symptoms of sexual dysfunction dyspareunia painful intercourse'
    if i==18300:
        return 'acne or pimples bad complexion blackheads blemishes breaking out complexion nos whiteheads'
    if i==18350:
        return 'discoloration or abnormal pigmentation birthmark blotches circles under eyes freckles redness spots'
    if i==18400:
        return 'infections of skin nos draining wound infected blister infected wound'
    if i==18401:
        return 'infection of skin of head or neck area'
    if i==18402:
        return 'infection of skin of arm hand or finger'
    if i==18403:
        return 'infection of skin of leg foot or toe'
    if i==18450:
        return 'symptoms of skin moles skin mole nos'
    if i==18451:
        return 'change in mole size or color'
    if i==18452:
        return 'bleeding mole'
    if i==18500:
        return 'warts nos condyloma condyloma acuminatum'
    if i==18550:
        return 'other growths of skin callus corns cysts nos cyst scalp skin growth nos skin tag'
    if i==18600:
        return 'skin rash rash skin eruption'
    if i==18601:
        return 'diaper rash'
    if i==18650:
        return 'skin lesion nos blister face lesion papule pustule raw area sore ulcer'
    if i==18700:
        return 'skin irritations nec skin pain skin itching'
    if i==18750:
        return 'swelling of skin bumps lumps nodules welts skin tumor'
    if i==18800:
        return 'other symptoms referable to skin'
    if i==18801:
        return 'skin oiliness'
    if i==18802:
        return 'skin dryness peeling scaliness roughness'
    if i==18803:
        return 'wrinkles'
    if i==18850:
        return 'symptoms referable to nails'
    if i==18851:
        return 'infected nail'
    if i==18852:
        return 'ingrown nail'
    if i==18853:
        return 'brittle breaking splitting cracked ridged nail'
    if i==18900:
        return 'symptoms referable to scalp scalp lesion'
    if i==18901:
        return 'too little hair alopecia baldness falling out losing hair'
    if i==18902:
        return 'unwanted hair abnormal hairiness hirsutism superfluous hair'
    if i==18903:
        return 'dryness flaky scalp dry scalp'
    if i==18904:
        return 'itching scalp'
    if i==18904:
        return 'navel problems umbilicus not healing navel protrusion'
    if i==19000:
        return 'neck symptoms'
    if i==19001:
        return 'neck pain ache soreness discomfort'
    if i==19002:
        return 'neck cramps contractures spasms'
    if i==19003:
        return 'neck limitation of movement stiffness tightness weakness'
    if i==19004:
        return 'neck weakness'
    if i==19005:
        return 'neck swelling'
    if i==19006:
        return 'neck lump mass tumor'
    if i==19050:
        return 'back symptoms'
    if i==19051:
        return 'back pain ache soreness discomfort'
    if i==19052:
        return 'back cramps contractures spasms'
    if i==19053:
        return 'back limitation of movement stiffness tightness weakness'
    if i==19054:
        return 'back weakness'
    if i==19055:
        return 'back swelling'
    if i==19056:
        return 'back lump mass tumor'
    if i==19100:
        return 'low back symptoms'
    if i==19101:
        return 'low back pain ache soreness discomfort'
    if i==19102:
        return 'low back cramps contractures spasms'
    if i==19103:
        return 'low back limitation of movement stiffness tightness weakness'
    if i==19104:
        return 'low back weakness'
    if i==19105:
        return 'low back swelling'
    if i==19106:
        return 'low back lump mass tumor'
    if i==19150:
        return 'hip symptoms'
    if i==19151:
        return 'hip pain ache soreness discomfort'
    if i==19152:
        return 'hip cramps contractures spasms'
    if i==19153:
        return 'hip limitation of movement stiffness tightness weakness'
    if i==19154:
        return 'hip weakness'
    if i==19155:
        return 'hip swelling'
    if i==19156:
        return 'hip lump mass tumor'
    if i==19200:
        return 'leg symptoms'
    if i==19201:
        return 'leg pain ache soreness discomfort'
    if i==19202:
        return 'leg cramps contractures spasms'
    if i==19203:
        return 'leg limitation of movement stiffness tightness weakness'
    if i==19204:
        return 'leg weakness'
    if i==19205:
        return 'leg swelling'
    if i==19206:
        return 'leg lump mass tumor'
    if i==19250:
        return 'knee symptoms'
    if i==19251:
        return 'knee pain ache soreness discomfort'
    if i==19252:
        return 'knee cramps contractures spasms'
    if i==19253:
        return 'knee limitation of movement stiffness tightness weakness'
    if i==19254:
        return 'knee weakness'
    if i==19255:
        return 'knee swelling'
    if i==19256:
        return 'knee lump mass tumor'
    if i==19300:
        return 'ankle symptoms'
    if i==19301:
        return 'ankle pain ache soreness discomfort'
    if i==19302:
        return 'ankle cramps contractures spasms'
    if i==19303:
        return 'ankle limitation of movement stiffness tightness weakness'
    if i==19304:
        return 'ankle weakness'
    if i==19305:
        return 'ankle swelling'
    if i==19306:
        return 'ankle lump mass tumor'
    if i==19350:
        return 'foot and toe symptoms'
    if i==19351:
        return 'foot and toe pain ache soreness discomfort'
    if i==19352:
        return 'foot and toe cramps contractures spasms'
    if i==19353:
        return 'foot and toe limitation of movement stiffness tightness weakness'
    if i==19354:
        return 'foot and toe weakness'
    if i==19355:
        return 'foot and toe swelling'
    if i==19356:
        return 'foot and toe lump mass tumor'
    if i==19400:
        return 'shoulder symptoms'
    if i==19401:
        return 'shoulder pain ache soreness discomfort'
    if i==19402:
        return 'shoulder cramps contractures spasms'
    if i==19403:
        return 'shoulder limitation of movement stiffness tightness weakness'
    if i==19404:
        return 'shoulder weakness'
    if i==19405:
        return 'shoulder swelling'
    if i==19406:
        return 'shoulder lump mass tumor'
    if i==19450:
        return 'arm symptoms'
    if i==19451:
        return 'arm pain ache soreness discomfort'
    if i==19452:
        return 'arm cramps contractures spasms'
    if i==19453:
        return 'arm limitation of movement stiffness tightness weakness'
    if i==19454:
        return 'arm weakness'
    if i==19455:
        return 'arm swelling'
    if i==19456:
        return 'arm lump mass tumor'
    if i==19500:
        return 'elbow symptoms'
    if i==19501:
        return 'elbow pain ache soreness discomfort'
    if i==19502:
        return 'elbow cramps contractures spasms'
    if i==19503:
        return 'elbow limitation of movement stiffness tightness weakness'
    if i==19504:
        return 'elbow weakness'
    if i==19505:
        return 'elbow swelling'
    if i==19506:
        return 'elbow lump mass tumor'
    if i==19550:
        return 'wrist symptoms'
    if i==19551:
        return 'wrist pain ache soreness discomfort'
    if i==19552:
        return 'wrist cramps contractures spasms'
    if i==19553:
        return 'wrist limitation of movement stiffness tightness weakness'
    if i==19554:
        return 'wrist weakness'
    if i==19555:
        return 'wrist swelling'
    if i==19556:
        return 'wrist lump mass tumor'
    if i==19600:
        return 'hand and finger symptoms wring stuck on finger'
    if i==19601:
        return 'hand and finger pain ache soreness discomfort'
    if i==19602:
        return 'hand and finger cramps contractures spasms'
    if i==19603:
        return 'hand and finger limitation of movement stiffness tightness weakness'
    if i==19604:
        return 'hand and finger weakness'
    if i==19605:
        return 'hand and finger swelling'
    if i==19606:
        return 'hand and finger lump mass tumor'
    if i==19650:
        return 'symptoms of unspecified muscles'
    if i==19651:
        return 'unspecified muscle pain ache soreness discomfort'
    if i==19652:
        return 'unspecified muscle cramps contractures spasms'
    if i==19653:
        return 'unspecified muscle limitation of movement stiffness tightness weakness'
    if i==19654:
        return 'unspecified muscle weakness'
    if i==19655:
        return 'unspecified muscle swelling'
    if i==19656:
        return 'unspecified muscle lump mass tumor'
    if i==19700:
        return 'symptoms of unspecified joints'
    if i==19701:
        return 'unspecified joint pain ache soreness discomfort'
    if i==19702:
        return 'unspecified joint cramps contractures spasms'
    if i==19703:
        return 'unspecified joint limitation of movement stiffness tightness weakness'
    if i==19704:
        return 'unspecified joint weakness'
    if i==19705:
        return 'unspecified joint swelling'
    if i==19706:
        return 'unspecified joint lump mass tumor'
    if i==19750:
        return 'musculoskeletal deformities crooked back hammer toe'
    if i==19751:
        return 'bowlegged knock-kneed'
    if i==19752:
        return 'posture problems'
    if i==19753:
        return 'pigeon-toed feet turn in'
    if i==19800:
        return 'other musculoskeletal symptoms bone pain stump pain'
    if i==20050:
        return 'intestinal infectious diseases cholera dysentery enteritis gastroenteritis giardia salmonella'
    if i==20100:
        return 'streptococcal infection streptococcal tonsillitis scarlet fever'
    if i==20150:
        return 'viral diseases chickenpox genital warts germal measles rubella hepatitis infections and nos herpes simplex infectious mononucleosis measles viral meningitis mumps plantar\'s warts poliomyelitis pps rabies respiratory synctival virus rsv shingles herpes zoster smallpox nos veneral warts verruca'
    if i==20151:
        return 'human immunodeficiency virus (hiv) with or without associated conditions acquired immunodeficiency syndrome aids aids-like syndrome aids-related complex arc hiv positive'
    if i==20152:
        return 'hemorrhagic fevers botulism ebola hemorrhagic fevers marburg'
    if i==20200:
        return 'sexually transmitted diseases chlamydia gonorrhea syphilis'
    if i==20250:
        return 'fungus infections (mycoses) athlete\'s foot candidiasis monilia dermatophytoses moniliasis ringworm thrush tinea yeast infection'
    if i==20300:
        return 'parasitic diseases ascaris leeches lice maggots pinworms scabies'
    if i==20310:
        return 'sepsis septicemia'
    if i==20350:
        return 'other and unspecified infectious and parasitic diseases bacterial infection behcet\'s syndrome cattleman\'s disease e coli lyme disease pcp pneumocystis carinii plague staphylococcal infections trichomonas vaginitis tuberculosis tularemia'
    if i==21000:
        return 'cancer gastrointestinal tract colon esophagus liver small intestine stomach'
    if i==21050:
        return 'cancer respiratory tract bronchus larynx lung throat trachea'
    if i==21100:
        return 'cancer skin and subcutaneous tissues basal cell carcinoma melanoma squamous cell carcinoma'
    if i==21150:
        return 'cancer breast'
    if i==21200:
        return 'cancer female genital tract cervix endomedtrium fallopian tubes ovary uterus vagina vulva'
    if i==21250:
        return 'cancer male genital tract epididymitis penis prepuce foreskin prostate scrotum spermatic cord testes'
    if i==21260:
        return 'cancer of urinary tract bladder kidney renal pelvis ureter urethra'
    if i==21300:
        return 'other malignant neoplasms bone cancer metastatic carcinoma brain tumor carcinoma in situ nos'
    if i==21350:
        return 'hodgkin\'s disease lymphomas leukemias cancer of blood lymphosarcoma multiple myeloma polycythemia vera'
    if i==21400:
        return 'fibroids and other uterine neoplasms cervical polyp leiomyomata myoma nabothian cyst'
    if i==21450:
        return 'other benign neoplasms bartholin\'s cyst dermoid cyst ovary hemangioma lipoma nasal polyp nevus ovarian cyst rectal polyp vaginal inclusion vocal cord'
    if i==21500:
        return 'neoplasm of uncertain nature myelodysplasia plasmacytoma'
    if i==22000:
        return 'diseases of the thyroid gland goiter hyperthyroidism hypothyroidism myxedema thyroid nodule thyrotoxicosis'
    if i==22050:
        return 'diabetes mellitus'
    if i==22100:
        return 'gout hyperuricemia'
    if i==22150:
        return 'other endocrine nutritional metabolic and immunity diseases amyloidosis barter\'s syndrome calcium deficiency cystinosis disorders of intestinal absorption electrolyte imbalance female hormone deficiency hematochromatosis elevated hl hormone imbalance hypercholesterolemia hyperlipidemia hypoglycemia impaired immune system iron deficiency low blood sugar malnutrition ovarian dysfunction poor nutrition sugar reaction wilson\'s syndrome'
    if i==22500:
        return 'anemia anemia nos iron deficiency anemia pernicious anemia sickle cell anemia'
    if i==22550:
        return 'other diseases of blood and blood-forming organs hemophilia hs purpura pancytopenia thrombocytopenia von willebrand\'s disease'
    if i==23000:
        return 'organic psychoses alcoholic psychoses drug withdrawal organic brain syndromes senile dementia'
    if i==23050:
        return 'functional psychoses autism bipolar disorder major depression manic-depressive psychoses paranoid states psychosis nos schizophrenia'
    if i==23100:
        return 'neuroses anxiety reaction depressive neurosis depressive reaction neurosis nos obsessive compulsive neurosis'
    if i==23150:
        return 'personality and character disorders'
    if i==23200:
        return 'alcoholism alcohol dependence'
    if i==23210:
        return 'drug dependence drug addiction nicorette dependency'
    if i==23250:
        return 'mental retardation'
    if i==23300:
        return 'other and unspecified mental disorders adolescent adjustment reaction attention deficit disorder add attention deficit hyperactivity disorder adhd bruxism mental dyslexia eating disorder grief reaction sexual deviations transient situational disturbances'
    if i==23500:
        return 'multiple sclerosis'
    if i==23550:
        return 'parkinson\'s disease (paralysis agitans)'
    if i==23600:
        return 'epilepsy'
    if i==23650:
        return 'migraine headache'
    if i==23700:
        return 'other and unspecified diseases of the nervous system acute lateral sclerosis alzheimer\'s disease bell\'s palsy carpal tunnel syndrome demyelinating disease guillain-barre meningitis morton\'s neuroma muscular dystrophy myasthenia gravis neurofibromatosis neuropathy paralysis nec phantom limb leg pain thoracic outlet syndrome tourette\'s syndrome'
    if i==24000:
        return 'inflammatory diseases of the eye blepharitis conjunctivitis ophthalmia iritis keratitis sicca sty eye ulcer'
    if i==24050:
        return 'refractive error anisometropia astigmatism hyperopia farsightedness myopia nearsightedness presbyopia'
    if i==24100:
        return 'cataract'
    if i==24150:
        return 'glaucoma glaucoma suspect hypertensive ocular disease increased ocular pressure'
    if i==24200:
        return 'other diseases of the eye amaurosis fugax amblyopia aphakia color blindness esotropia exotropia krukenberg\'s syndrome macular degeneration pterygium retinal detachment strabismus'
    if i==24500:
        return 'otitis media'
    if i==24550:
        return 'other diseases of the ear ear abcses labyrinthitis meniere\'s disease ruptured tympanic membrane'
    if i==25000:
        return 'rheumatic fever and chronic rheumatic heart disease chorea'
    if i==25050:
        return 'hypertension with involvement of target organs hcd hcvd hypertensive cardiovascular disease hypertensive heart disease pulmonary hypertension renal hypertension'
    if i==25100:
        return 'hypertension hypertensive high blood pressure'
    if i==25150:
        return 'ischemic heart disease angina pectoris arteriosclerotic cardiovascular disease acvd arteriosclerotic heart disease ashd coronary coronary heart disease heart attack myocardial infarction'
    if i==25200:
        return 'other heart disease aortic valve stenosis arrhythmia nos atrial fibrillation cardiac arrhythmia cardiac dysrhythmias cardiomyopathy congestive cardiomyopathy congestive heart failure cor pulmonale heart failure heart murmur mitral valve prolapse mitral valve regurgitation paroxysmal tachycardia premature ventricular contractions pvc ventricular tachycardia'
    if i==25250:
        return 'cerebrovascular disease carotid stenosis cerebral arteriosclerosis cerebral hemorrhage cerebral stenosis cerebrovascular accident stroke tia'
    if i==25400:
        return 'atherosclerosis arteriosclerosis hardening of the arteries'
    if i==25350:
        return 'phlebitis thrombophlebitis phlebothrombosis'
    if i==25400:
        return 'varicose veins'
    if i==25450:
        return 'hemorrhoids perineal tags'
    if i==25500:
        return 'other disease of circulatory system aneurysm artery disease blood clots pulmonary embolism heart disease nos infarct nos lymphadenitis lymphadenopathy postphlebitic syndrome raynaud\'s disease stasis dermatitis temporal arteritis vasculitis venous insufficiency'
    if i==26000:
        return 'upper respiratory infections except tonsillitis croup laryngitis pharyngitis rhinitis sinusitis'
    if i==26050:
        return 'tonsillitis'
    if i==26100:
        return 'bronchitis acute bronchitis bronchitis nos chronic bronchitis'
    if i==26200:
        return 'emphysema'
    if i==26250:
        return 'asthma'
    if i==26300:
        return 'pneumonia bacterial pneumonia bronchopneumonia pneuomonitis viral pneumonia'
    if i==26350:
        return 'hay fever allergic rhinitis dust allergy pollen allergy animal allergy ragweed allergy nasal allergy pollenosis'
    if i==26400:
        return 'other respiratory diseases bronchiolitis bronchospasm chronic obstructive pulmonary disease deviated nasal septum hemothorax other respiratory problems pleurisy pneumothorax pulmonary edema respiratory failure sars'
    if i==26500:
        return 'diseases of the esophagus stomach and duodenum barrett\'s esophagus duodenal ulcer esophageal ulcer esophagitis gastritis gerd peptic ulcer reflux stomach ulcer'
    if i==26550:
        return 'appendicitis'
    if i==26600:
        return 'hernia of the abdominal cavity abdominal hernia femoral hernia hiatus hernia inguinal hernia umbilical hernia ventral hernia'
    if i==26650:
        return 'diseases of the intestine and peritoneum rectal abscess adhesions crohn\'s disease diverticulitis diverticulosis rectal anal fissure rectal anal fistula ileitis irritable bowel syndrome proctitis small bowel obstruction spastic colitis ulcerative colitis'
    if i==26700:
        return 'diseases of the liver gallbladder and pancreas biliary colic cholecystitis cholelithiasis gallstones cirrhosis liver diseases pancreatitis'
    if i==26750:
        return 'other diseases of digestive system nec mandibular cyst'
    if i==26751:
        return 'dental abscess'
    if i==26752:
        return 'dental cavities'
    if i==26753:
        return 'canker sore'
    if i==26754:
        return 'stomatitis'
    if i==26755:
        return 'temperomandibular joint tmj pain'
    if i==26756:
        return 'temperomandibular joint tmj syndrome'
    if i==27000:
        return 'cystitis'
    if i==27050:
        return 'urinary tract disease except cystitis bladder stones glomerulonephritis glomerulonephrosis kidney cyst kidney stones neurogenic bladder pyelonephritis renal failure ureteral calculus urethritis urolithiasis'
    if i==27100:
        return 'diseases of the male genital organs benign prostatic hypertrophy bph epididymitis include hydrocele peyronie\'s disease phimosis prostatitis'
    if i==27150:
        return 'fibrocystic and other diseases of breast breast abscess mastitis'
    if i==27200:
        return 'pelvic inflammatory disease (pid) oophoritis pelvic peritonitis salpingitis'
    if i==27250:
        return 'cervicitis vaginitis cervical erosion vulvovaginitis'
    if i==27300:
        return 'other diseases of female reproductive system cervical dysplasia cystocele dysfunctional uterine bleeding endometriosis polycystic ovaries procidentia uteri prolapse of the uterus rectal-vaginal fistula rectocele vulvitis'
    if i==27350:
        return 'diagnosed complications of pregnancy and puerperium advanced maternal age diabetes during pregnancy ectopic pregnancy edema of pregnancy fetal death in utero gallstones high blood pressure during pregnancy hyperemesis intrauterine growth retardation iugr miscarriage multiple pregnancy placenta previa post dates previous c-section rh sensitization spontaneous abortion threatened abortion toxemia adolescent twins young maternal age'
    if i==27360:
        return 'other diseases of the genitourinary system nec'
    if i==28000:
        return 'carbuncle furuncle boil cellulitis abscess nec'
    if i==28050:
        return 'impetigo'
    if i==28100:
        return 'seborrheic dermatitis dandruff'
    if i==28150:
        return 'eczema and dermatitis nos allergic dermatitis'
    if i==28200:
        return 'psoriasis'
    if i==28250:
        return 'other diseases of the skin allergic skin reactions epidermal inclusion cyst folliculitis hidradenitis hives keloid keratosis lupus erythematosus nos paronychia pilonidal cyst poison ivy poison oak rosacea sebaceous cyst urticaria'
    if i==29000:
        return 'arthritis osteoarthritis rheumatism nos rheumatoid arthritis septic arthritis'
    if i==29050:
        return 'nonarticular rheumatism bursitis ganglion cyst lumbago myositis polymyalgia theumatica radiculitis radiculopathy synovitis tendinitis tenosynovitis'
    if i==29100:
        return 'other musculoskeletal or connective tissue disease baker\'s cyst bone cysts bone spur bunions cervical myelopathy curvatures of spine degenerative disc diseases dupuytren\'s contracture exostosis kyphoscoliosis kyphosis  osteomyelitis osteoporosis paget\'s plantar fistula scleroderma scoliosis sjogen\'s slipped disc spondylosis spur nos systemic lupus erythematosus'
    if i==29500:
        return 'congenital anomalies of heart and circulatory system'
    if i==29550:
        return 'undescended testicles hypospadias'
    if i==29600:
        return 'other and unspecified congenital anomalies absence of organs blocked tear duct cleft palate cleft lip clubfoot congenital dislocation of hip deformed earlobe down syndrome duplication of organs harelip mitochondrial disorders turner\'s syndrome'
    if i==29800:
        return 'prematurity late effects of prematurity premature infant'
    if i==29900:
        return 'all other perinatal conditions'
    if i==31000:
        return 'general medical examination annual exam checkup nos checkup routine evaluation nos general exam healthy adult healthy child history and physical multiphasic screening exam physical exam preventative regular exam routine exam pre-op exam'
    if i==31050:
        return 'well baby examination'
    if i==31300:
        return 'general psychiatric or psychological examination psychological testing'
    if i==32000:
        return 'pregnancy unconfirmed hcg late menses late menstruation might be pregnant missed period period late possible pregnancy pregnancy test'
    if i==32050:
        return 'prenatal examination normal antepartum visit pregnancy nos routine obstetrical care'
    if i==32150:
        return 'postpartum examination routine'
    if i==32200:
        return 'breast examination'
    if i==32250:
        return 'gynecological examination pelvic exam examination involving iud repeat or abnormal pap smear'
    if i==32300:
        return 'eye examination check contacts check glasses for contacts for glasses glasses nos grid need new glasses no change in vision routine ophthalmologic exam test for nearsightedness farsightedness to test my eyes vision about the same visual field test'
    if i==32350:
        return 'heart examination cardiac care cardiac checkup heart checkup'
    if i==32400:
        return 'other special examination aicd check check tubes examination of functioning internal prosthetic devices implants shunts stents hearing aid icd check neurological exam pacemaker check thyroid'
    if i==33000:
        return 'sensitization test allergy test'
    if i==33050:
        return 'skin immunity test ppd test tuberculin test'
    if i==33100:
        return 'glucose level determination hbg a1c-glycolosated hemoglobin inclues blood sugar test check sugar glucose intolerance test test for diabetes'
    if i==33140:
        return 'human immunodeficiency virus (hiv) test aids test'
    if i==33150:
        return 'other blood test blood alcohol blood count blood culture blood test nos blood thinning test cbc check cholesterol prothrombin time psa sickle cell anemia test'
    if i==33151:
        return 'blood test for sexually transmitted disease'
    if i==33250:
        return 'urine test estriol for fetal evaluation test urine for sugar urinalysis urine culture'
    if i==33300:
        return 'diagnostic endoscopies arthroscopy cystoscopy laparoscopy proctoscopy sigmoidoscopy'
    if i==33350:
        return 'biopsies'
    if i==33400:
        return 'mammography xerography breast thermography'
    if i==33450:
        return 'diagnostic radiology angiogram angiography bone density bone scan ct scan hysterosalpingogram ivp mri myelogram radioisotope scanning venogram x-ray'
    if i==33500:
        return 'ekg ecg electrocardiogram treadmill stress testing holter monitor'
    if i==33550:
        return 'eeg electroencephalogram'
    if i==33600:
        return 'hearing test hearing exam'
    if i==33650:
        return 'pap smear'
    if i==33660:
        return 'nasal swab'
    if i==33700:
        return 'other and unspecified diagnostic tests amniocentesis centesis cervicitis drug screening echocardiogram electronic fetal monitoring exposure to pid lab test nos pulmonary function test spinal tap ultrasound'
    if i==33701:
        return 'glaucoma test atn check check intraocular pressure'
    if i==33702:
        return 'throat culture'
    if i==33703:
        return 'heart catherization'
    if i==33704:
        return 'other cultures skin culture'
    if i==34000:
        return 'prophylactic inoculations flu shot fu vaccine immunization influenza shot rhogam tetanus shot vaccination'
    if i==34050:
        return 'exposure to sexually transmitted disease check for std may have std'
    if i==34080:
        return 'possible hiv'
    if i==34090:
        return 'exposure to other infections diseases chickenpox infectious hepatitis measles mumps pathogens includes-tubercolosis'
    if i==34150:
        return 'exposure to bodily fluids of another person nos blood exposure exposure to another\'s secretions'
    if i==35000:
        return 'family planning nos birth control nos counseling examinations general advice unwanted pregnancy contraceptive'
    if i==35050:
        return 'contraceptive medication depo provera birth control pills contraceptive implants foams jellies oral contraceptives renewing pill prescription norplant checkup norplant insertion removal'
    if i==35100:
        return 'contraceptive device diaphragm iud'
    if i==35150:
        return 'counseling and examinations for pregnancy interruption evaluation for an arrangement for abortion wants abortion'
    if i==35250:
        return 'abortion to be performed'
    if i==35250:
        return 'sterilization and sterilization to be performed vasectomy tubal ligation'
    if i==35300:
        return 'artificial insemination assisted reproductive technologies fetal reduction intrauterine insemination in vitro fertilization'
    if i==35350:
        return 'preconception counseling and education artificial insemination desires pregnancy egg donor infertility monitoring cycles semen analysis sperm donor sperm washing tubal reversal'
    if i==41000:
        return 'allergy medication allergy shots allergy treatments allergy testing'
    if i==41100:
        return 'injections antibiotics fat hormones injections nos iron lupron depot shots nos steroid vitamins'
    if i==41110:
        return 'noncompliance with medication therapy'
    if i==41150:
        return 'medication other and unspecified kinds antibiotics nos check medication drug studies for medication hormone refill medication for pain oral placebo effect prescribe medication renew prescription renew scripts scripts'
    if i==42000:
        return 'preoperative visit for specified and unspecified types of surgery discuss any surgery discussion of cosmetic surgery pre-op examination surgical consultation'
    if i==42050:
        return 'postoperative visit check graft check implant check shunt check stoma check surgical wound clotted graft shunt endoscopy follow-up fu endoscopy postop care postop pain postop suture removal suture removal follow-up'
    if i==44000:
        return 'physical medicine and rehabilitation back adjustment cardiac rehabilitation heat therapy hydrotherapy occupational therapy physical therapy pulmonary rehabilitation recreational therapy speech therapy therapeutic exercises vocational rehabilitation'
    if i==44010:
        return 'cardiopulmonary resuscitation cpr'
    if i==44050:
        return 'respiratory therapy asthma treatment inhalation therapy inhaler breathing treatment'
    if i==44100:
        return 'psychotherapy group counseling family therapy group therapy psychoanalysis'
    if i==44150:
        return 'radiation therapy sp'
    if i==44200:
        return 'acupuncture'
    if i==44250:
        return 'chemotherapy'
    if i==45000:
        return 'tube insertion chest tube flushed catheter g-tube peg picc port-a-cath trach'
    if i==45050:
        return 'cauterization'
    if i==45070:
        return 'iv therapy infusion'
    if i==45100:
        return 'urinary tract instrumentation and catheterization flushed urinary catheter urethral dilation urinary catheterization'
    if i==45150:
        return 'fitting glasses and contact lenses broken or lost glasses contacts clean glasses contacts pick up glasses contacts prescription renewal'
    if i==45180:
        return 'detoxification'
    if i==45181:
        return 'alcohol detoxification'
    if i==45182:
        return 'drug detoxification'
    if i==45200:
        return 'minor surgery ear tube removal ears pierced joint manipulation norplant insertion removal ring removal tattoo removal tube removal'
    if i==45201:
        return 'wart removed'
    if i==45210:
        return 'major surgery aspiration bone marrow balloon angiogram cervical conization cholecystectomy eye laser surgery lens extraction liver biopsy percutaneous transluminal angiogram polypection ptca'
    if i==45250:
        return 'kidney dialysis'
    if i==45290:
        return 'internal prosthetic devices breast implants cardiac pacemaker joint prostheses vns'
    if i==45300:
        return 'external prosthetic devices artificial body parts'
    if i==45350:
        return 'corrective appliances back brace dental cap crown earplugs eye patch hearing aid jobst or ted stockings leg brace neck brace orthopedic shoes walking cane'
    if i==45400:
        return 'cast splint'
    if i==45450:
        return 'dressing bandage'
    if i==45500:
        return 'irrigation lavage'
    if i==45550:
        return 'suture'
    if i==45560:
        return 'cosmetic injection'
    if i==45561:
        return 'botox injection'
    if i==45562:
        return 'collagen injection'
    if i==45600:
        return 'other specific therapeutic procedures nec adjust device apheresis cardioversion cryotherapy cut toe nails debridement earwick ect enema epidural eye exercises insulin pump joint injection nerve block pessary phototherapy sclerotherapy skin rejuvenation tens unit ultraviolet treatment wound care nos'
    if i==45650:
        return 'transplants nos stem cell'
    if i==45651:
        return 'transplant failure bone marrow'
    if i==46000:
        return 'diet and nutritional counseling check weight counseling for weight reduction'
    if i==46040:
        return 'human immunodeficiency virus (hiv) counseling aids counseling aids information education arc counseling worried about getting transmitting aids'
    if i==46050:
        return 'medical counseling nos alcohol disease counseling drug drug rehabilitation locate advocate medical consultation new patient open house patient education personal problem questions about condition referral relapse prevention schedule test or study second opinion to learn about a condition to meet doctor trouble toilet training wants to talk to doctor'
    if i==46051:
        return 'family history of cardiovascular disease'
    if i==46052:
        return 'family history of cancer'
    if i==46053:
        return 'family history of diabetes'
    if i==46054:
        return 'family history of other disease or condition'
    if i==47000:
        return 'economic problem can\'t pay bills too little income'
    if i==47020:
        return 'problem with access to medical care blocked access to medical care care not covered by insurance insurance problem limited access to medical care'
    if i==47050:
        return 'marital problems alcoholic spouse custody battle divorce desertion separation marriage counseling nos premarital counseling problem with husband wife'
    if i==47100:
        return 'parent-child problems adopted or foster child concern about childhood behavior discipline maturation problems oppositional defiance working mother'
    if i==47150:
        return 'other problems of family relationship aged parents or inlaws brother sister difficulty divorced parents family fights and disruptions problems with relatives'
    if i==47200:
        return 'education problems absenteeism truancy hates school problems with teachers school behavior problems'
    if i==47250:
        return 'occupational problems job dissatisfaction out of work problem with boss or coworkers unable to work unemployment'
    if i==47300:
        return 'social adjustment problems discrimination problems don\'t have any friends loneliness neighborhood problems social isolation'
    if i==47350:
        return 'legal problems imprisonment prosecution lawsuits litigation'
    if i==47351:
        return 'police involvement in outpatient visit circumstances brought by police police called'
    if i==47400:
        return 'other social problems disabled disappointment in others disasters homeless housing and clothing problems pregnancy out-of-wedlock problem with boyfriend girlfriend problems of aging relationship problems'
    if i==48000:
        return 'progress visit nos chronic nos followup nos getting better same worse monthly visit ongoing treatment nos recheck revisit routine followup same problems nos touching base'
    if i==50050:
        return 'head and face fractures and dislocations facial bones jaw nose skull'
    if i==50100:
        return 'spinal column fractures and dislocations back neck vertebrae'
    if i==50150:
        return 'trunk area except spinal column fractures and dislocations clavicle collarbone pelvic scapula rib'
    if i==50200:
        return 'leg fractures and dislocations femur fibula hip knee tibia'
    if i==50250:
        return 'ankle fractures and dislocations'
    if i==50300:
        return 'foot and toe fractures and dislocations'
    if i==50350:
        return 'arm fractures and dislocations elbow humerus radius shoulder ulna'
    if i==50400:
        return 'wrist fractures and dislocations'
    if i==50450:
        return 'hand and finger fractures and dislocations'
    if i==50500:
        return 'fracture other and unspecified'
    if i==51050:
        return 'cervical spine and neck sprains and strains whiplash'
    if i==51100:
        return 'back strains and sprains'
    if i==51150:
        return 'knee strains and sprains'
    if i==51200:
        return 'ankle strains and sprains'
    if i==51250:
        return 'wrist strains and sprains'
    if i==51300:
        return 'sprain or strain other and unspecified'
    if i==52050:
        return 'head and neck area lacerations and cuts'
    if i==52100:
        return 'facial area lacerations and cuts eye ear forehead lip nose'
    if i==52150:
        return 'trunk area lacerations and cuts perineum'
    if i==52200:
        return 'lower extremity lacerations and cuts ankle foot'
    if i==52250:
        return 'upper extremity lacerations and cuts arm fingers hand wrist'
    if i==52300:
        return 'lacerations and cuts site unspecified'
    if i==53050:
        return 'head neck and facial area puncture wounds'
    if i==53100:
        return 'trunk area puncture wounds'
    if i==53150:
        return 'lower extremity puncture wounds'
    if i==53200:
        return 'upper extremity puncture wounds'
    if i==53250:
        return 'puncture wound site unspecified needlestick nos'
    if i==54050:
        return 'head neck and face contusions abrasions and bruises'
    if i==54100:
        return 'eye contusions abrasions and bruises black eye contusion corneal abrasion'
    if i==54150:
        return 'trunk area contusions abrasions and bruises injury to scrotum'
    if i==54200:
        return 'lower extremity contusions abrasions and bruises'
    if i==54250:
        return 'upper extremity contusions abrasions and bruises'
    if i==54300:
        return 'contusions abrasions and bruises site unspecified'
    if i==55050:
        return 'head neck and face other and unspecified injury post concussive syndrome tooth fracture tooth knocked out traumatic brain injury tbi'
    if i==55100:
        return 'eye other and unspecified injury'
    if i==55150:
        return 'back other and unspecified injury'
    if i==55200:
        return 'chest and abdomen other and unspecified injury internal injuries'
    if i==55250:
        return 'hip other and unspecified injury'
    if i==55350:
        return 'knee other and unspecified injury'
    if i==55400:
        return 'ankle other and unspecified injury'
    if i==55450:
        return 'foot and toe other and unspecified injury'
    if i==55500:
        return 'shoulder other and unspecified injury'
    if i==55550:
        return 'arm other and unspecified injury'
    if i==55600:
        return 'elbow other and unspecified injury'
    if i==55650:
        return 'wrist other and unspecified injury'
    if i==55700:
        return 'hand and finger other and unspecified injury'
    if i==55750:
        return 'injury multiple or unspecified includes post-traumatic headache'
    if i==56000:
        return 'foreign body in eye'
    if i==56050:
        return 'foreign body in nose'
    if i==56100:
        return 'foreign body in skin'
    if i==56150:
        return 'foreign body in digestive tract mouth rectum throat'
    if i==56160:
        return 'foreign body in respiratory tract'
    if i==56200:
        return 'other and unspecified sites of foreign body'
    if i==57050:
        return 'head neck face and eyes burns'
    if i==57150:
        return 'extremities burns upper lower'
    if i==57100:
        return 'trunk area burns'
    if i==57200:
        return 'burn site unspecified'
    if i==57500:
        return 'sunburn windburn'
    if i==57550:
        return 'insect bites sting tick'
    if i==57600:
        return 'animal snake human bites'
    if i==58000:
        return 'late effects of an old injury deformities scars'
    if i==58050:
        return 'motor vehicle accident auto car motorcycle'
    if i==58100:
        return 'accident nos fall'
    if i==58150:
        return 'violence nos abuse beat up in a fight stabbing'
    if i==58151:
        return 'child abuse or neglect'
    if i==58152:
        return 'battered spouse'
    if i==58153:
        return 'elder abuse'
    if i==58154:
        return 'gunshot wound'
    if i==58180:
        return 'intentional self-mutilation self abuse tried to hurt self'
    if i==58200:
        return 'suicide attempt'
    if i==58201:
        return 'intentional overdose'
    if i==58300:
        return 'rape sexual assault'
    if i==58301:
        return 'sexual abuse molestation'
    if i==58350:
        return 'dead on arrival (doa)'
    if i==58360:
        return 'respiratory arrest'
    if i==58370:
        return 'cardiac arrest code blue arrest'
    if i==58380:
        return 'drowning near drowning'
    if i==58390:
        return 'cardiopulmonary arrest'
    if i==58400:
        return 'unconscious on arrival coma found unconscous knocked out shock stupor unresponsive'
    if i==58410:
        return 'state of consciousness not specified brought in by ambulance found on floor verbally unresponsive'
    if i==58420:
        return 'altered level of consciousness nos'
    if i==59000:
        return 'unintentional poisoning'
    if i==59001:
        return 'food poisoning'
    if i==59002:
        return 'ingestion inhalation or exposure to potentially poisonous products heavy metal toxicity household products chemicals drugs gas smoke lead mace in eyes'
    if i==59052:
        return 'adverse effect of drug abuse bad trip nonsuicidal combination of drugs and alcohol drug-induced hallucinations freaked out on drugs ingestion of drugs for nonmedicial-purposes unintentional overdose'
    if i==59150:
        return 'adverse effect of alcohol acute intoxication drunk inclues intoxication'
    if i==59200:
        return 'adverse effects of environment air pollution frostbite hypothermia noise pollution sun damage sun poisoning too hot water pollution'
    if i==59210:
        return 'adverse effects of second-hand smoke'
    if i==59220:
        return 'adverse effects of terrorism and bioterrorism'
    if i==59250:
        return 'complications of surgical or medical procedures and treatments artificial openings catheter foreign body medical complications nos non-healing surgical wound post-op fever post-op hemorrhage post-op infection inflammation post-op sepsis shunt tubes wound dehiscence'
    if i==61000:
        return 'blood glucose tests abnormal glucose tolerance test elevated blood sugar glucose control high blood sugar hyperglycemia sugar in blood'
    if i==61050:
        return 'cholesterol and triglyceride tests high cholesterol'
    if i==61060:
        return 'human immunodeficiency virus (hiv) test results of aids test'
    if i==61100:
        return 'other blood tests elevated sed rate low potassium positive blood culture positive serology vdrl psa results'
    if i==62000:
        return 'results of urine tests abnormal urinalysis positive urine culture sugar in urine'
    if i==63000:
        return 'cytology findings abnormal pap smear atypical pap smear pap smear of cervix positive pap smear repeat pap smear'
    if i==64000:
        return 'radiological findings abnormal x-ray x-ray results xeromammography results'
    if i==65000:
        return 'results of ekg holter monitor review'
    if i==66000:
        return 'results of skin tests'
    if i==67000:
        return 'other and unspecified test results abnormal eeg abnormal lab test results nos abnormal scans abnormal pulmonary function test colonoscopy results ct scans failed hearing vision mri results of biopsy results of fetal evaluation tests discuss test results ultrasonography results'
    if i==71000:
        return 'physical exam required for school or employment'
    if i==71001:
        return 'physical exam required for employment preemployment exam required company physical return to work checkup teacher certificate physical'
    if i==71002:
        return 'executive physical examination'
    if i==71003:
        return 'physical exam required for school college daycare center grade school high school nurser school'
    if i==71004:
        return 'physical exam for extracurricular activites athletics boy scouts girl scouts camp little league'
    if i==71200:
        return 'driver\'s license exam dot'
    if i==71250:
        return 'insurance examination'
    if i==71300:
        return 'disability examination evaluation of disability social security examination'
    if i==71310:
        return 'worker\'s comp exam'
    if i==71350:
        return 'premarital examination'
    if i==71351:
        return 'premarital blood test'
    if i==71370:
        return 'direct admission to hospital admit to hospital direct admit for admission here for admission involuntary commitment preadmission evaluation preadmission exam voluntary commitment'
    if i==71400:
        return 'other reason for visit required by party other than the patient or the healthcare provider medical certificate physical certificate physical examination for adoption psychiatric examination required by court travel wic medical clearance'
    if i==89900:
        return 'problems complaints nec'
    if i==89910:
        return 'patient unable to speak english'
    if i==89930:
        return 'patient refused card left ama walked out'
    if i==89970:
        return 'entry of none or no complaint asymptomatic nos doing well feeling good'
    if i==89980:
        return 'insufficient information'
    if i==89990:
        return 'illegible entry'
    if i==-9:
        return 'blank entry'
    else:
        return 'other' 
    
