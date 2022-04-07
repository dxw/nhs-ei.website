# A list of all the new categories, with associated information used to create the category object.

# At the moment only `name` is supported information, but this may change in future.

# Changing a slug here will have potentially import-breaking consequences and should really only be done before a complete content refresh.

CATEGORIES = {
    "about-nhs-england": {"name": "About NHS England"},
    "ageing-well": {"name": "Ageing well"},
    "allied-health-professionals": {"name": "Allied Health Professionals"},
    "armed-forces": {"name": "Armed Forces"},
    "atlas": {"name": "Atlas"},
    "blogs": {"name": "Blogs"},
    "bulletins": {"name": "Bulletins"},
    "cancer": {"name": "Cancer"},
    "cardiovascular": {"name": "Cardiovascular"},
    "carers": {"name": "Carers"},
    "central-and-east-of-england": {"name": "Central and East of England"},
    "children-and-young-people": {"name": "Children and young people"},
    "commissioning": {"name": "Commissioning"},
    "community-and-social-care": {"name": "Community and social care"},
    "coronavirus": {"name": "Coronavirus"},
    "corporate-publications": {"name": "Corporate publications"},
    "dementia": {"name": "Dementia"},
    "dentistry-and-oral-health": {"name": "Dentistry and oral health"},
    "diabetes": {"name": "Diabetes"},
    "digital": {"name": "Digital"},
    "elective-care": {"name": "Elective care"},
    "emergency-preparedness-and-response": {
        "name": "Emergency preparedness and response"
    },
    "end-of-life-care": {"name": "End of life care"},
    "estates-and-healthcare-properties": {"name": "Estates and healthcare properties"},
    "events": {"name": "Events"},
    "finance": {"name": "Finance"},
    "gender-identity": {"name": "Gender identity"},
    "general-practice": {"name": "General Practice"},
    "get-involved": {"name": "Get involved"},
    "governance-and-standards": {"name": "Governance and standards"},
    "greener-nhs": {"name": "Greener NHS"},
    "health-and-justice": {"name": "Health and justice"},
    "healthcare-inequalities": {"name": "Healthecare inequalities"},
    "hearing-loss": {"name": "Hearing loss"},
    "improvement": {"name": "Improvement"},
    "innovation": {"name": "Innovation"},
    "integrated-care": {"name": "Integrated care"},
    "learning-disabilities": {"name": "Learning disabilities"},
    "london": {"name": "London"},
    "long-term-conditions": {"name": "Long term conditions"},
    "maternity-midwifery-and-neonatal": {"name": "Maternity, midwifery and neonatal"},
    "mental-health": {"name": "Mental health"},
    "midlands": {"name": "Midlands"},
    "networks-and-collaboration": {"name": "Networks and collaboration"},
    "news": {"name": "News"},
    "nhs-111": {"name": "NHS 111"},
    "nhs-providers": {"name": "NHS providers"},
    "nhs-standard-contract": {"name": "NHS standard contract"},
    "nhs-workforce": {"name": "NHS Workforce"},
    "north-east": {"name": "North East"},
    "north-west": {"name": "North West"},
    "nursing": {"name": "Nursing"},
    "obesity": {"name": "Obesity"},
    "older-people": {"name": "Older people"},
    "online-services": {"name": "Online services"},
    "optical": {"name": "Optical"},
    "patient-experience": {"name": "Patient experience"},
    "patient-safety-alert": {"name": "Patient safety alert"},
    "patient-safety": {"name": "Patient safety"},
    "personalised-care": {"name": "Personalised care"},
    "pharmacy-and-medicine": {"name": "Pharmacy and medicine"},
    "primary-care": {"name": "Primary care"},
    "public-health": {"name": "Public health"},
    "recruitment-and-retention": {"name": "Recruitment and retention"},
    "respiratory": {"name": "Respiratory"},
    "safety": {"name": "Safety"},
    "seven-day-services": {"name": "Seven day services"},
    "severe-weather-advice": {"name": "Severe weather advice"},
    "south-east": {"name": "South East"},
    "south-west": {"name": "South West"},
    "sexual-assault-and-abuse": {"name": "Sexual assault and abuse"},
    "statistics": {"name": "Statistics"},
    "stroke": {"name": "Stroke"},
    "sustainability": {"name": "Sustainability"},
    "training": {"name": "Training"},
    "urgent-and-emergency-care": {"name": "Urgent and emergency care"},
}

# Map a given Wordpress ID for a category type to slugs in the new categories list.

# A single string maps to one slug, an array of strings to multiple slugs.

# If a category is to be deleted, use an empty array.

CATEGORY_MAP = {
    "categories-commissioning": {
        "40": "bulletins",  # 6cs-live-bulletin
        "41": ["urgent-and-emergency-care", "statistics"],  # a-e-weekly-data
        "42": "statistics",  # abortion-statistics-for-england-and-wales
        "7": "about-nhs-england",  # about-us
        "43": "statistics",  # admission-events-referrals-and-attendances
        "112": "blogs",  # alistair-burns
        "44": [
            "allied-health-professionals",
            "bulletins",
        ],  # allied-health-professionals-bulletin
        "45": "statistics",  # ambulance-quality-indicators
        "113": "blogs",  # ann-driver
        "46": "statistics",  # annual-cancer-waiting-times-reports
        "114": "blogs",  # barbara-hakin
        "47": "statistics",  # bed-availability-and-occupancy
        "48": "blogs",
        "8": "corporate-publications",  # board-meetings
        "49": "statistics",  # breastfeeding-quarterly-statistical-releases
        "50": "bulletins",  # bulletin-for-ccgs
        "52": "corporate-publications",  # business-plan-quarterly-data-summaries
        "51": "corporate-publications",  # business-plan-2012-2015-indicators-and-other-key-data
        "9": "commissioning",  # ccg-learning-and-support-tool
        "10": "commissioning",  # ccg-learning-network-news
        "53": "statistics",  # cancelled-elective-operations
        "54": "statistics",  # central-alerting-system-data
        "56": "bulletins",  # chief-scientific-officer-bulletin
        "55": "bulletins",  # chief-nursing-officer-bulletin
        "57": "statistics",  # civil-service-people-survey-dh-results
        "58": "statistics",  # commissioner-based-waiting-times-for-cancer-patients
        "59": "bulletins",  # commissioning-support-bulletin
        "1243": [
            "training",
            "commissioning",
        ],  # conflicts-of-interest-audit-and-training
        "60": "statistics",  # consultant-led-referral-to-treatment-waiting-times-statistics
        "61": "statistics",  # critical-care-bed-capacity-and-cancelled-urgent-operations
        "66": "corporate-publications",  # dh-business-expenses
        "67": "corporate-publications",  # dh-complaints
        "62": "blogs",  # david-nicholson
        "63": "statistics",  # delayed-transfers-of-care
        "64": "corporate-publications",  # departmental-spending-over-25000
        "65": "corporate-publications",  # departmental-spending-over-500
        "68": "statistics",  # diagnostic-imaging-dataset
        "69": "statistics",  # diagnostics-waiting-times-and-activity-data
        "70": "statistics",  # direct-access-audiology-waiting-times
        "71": "blogs",  # dr-johnny-marshall
        "11": "nhs-workforce",  # everyone-counts
        "72": "corporate-publications",  # exceptions-to-spending-moratoria
        "12": "events",  # expo
        "13": [],  # extended-team
        "14": "statistics",  # friends-and-family-test
        "74": "statistics",  # gp-patient-survey
        "75": "statistics",  # gp-patient-survey-dental-statistics
        "73": "bulletins",  # gp-and-practice-team-bulletin
        "15": "governance-and-standards",  # governing-bodies
        "76": "blogs",  # guest-blogs
        "77": "statistics",  # hospital-estates-and-facilities-statistic
        "78": "improvement",  # impact-assessments
        "79": "blogs",  # inderjit-singh
        "17": [],  # individual-leaders
        "80": "bulletins",  # informed
        "81": "statistics",  # integrated-performance-measures-monitoring
        "82": "blogs",  # jane-cummings
        "83": "blogs",  # john-holden
        "84": "bulletins",  # liaison-and-diversion-bulletin
        "85": [],  # local-child-health-profiles
        "86": [],  # local-health-profiles
        "87": "blogs",  # martin-mcshane
        "88": "bulletins",  # medical-directors-bulletin
        "89": ["mental-health", "statistics"],  # mental-health-community-teams-activity
        "90": "blogs",  # mike-bewick
        "91": "blogs",  # mike-durkin
        "93": "corporate-publications",  # ministerial-visits
        "92": "corporate-publications",  # ministerial-gifts-hospitality
        "94": "statistics",  # mixed-sex-accommodation-breaches
        "95": "statistics",  # monthly-hospital-activity-data
        "97": "statistics",  # nhs-111-minimum-data-set
        "98": [
            "dentistry-and-oral-health",
            "commissioning",
        ],  # nhs-dental-commissioning
        "99": "statistics",  # nhs-staff-survey
        "96": "statistics",  # national-diet-and-nutrition-survey
        "18": "patient-safety",  # never-events
        "19": "news",
        "100": "finance",  # non-consolidated-performance-related-payments
        "101": "blogs",  # olivia-butterworth
        "105": "safety",  # pip-breast-implants
        "20": "safety",  # patient-safety-alerts
        "102": "patient-experience",
        "103": "finance",  # payment-of-suppliers
        "104": "corporate-publications",  # permanent-secretaries-meetings
        "1258": "primary-care",
        "106": [],  # public-health-outcomes-framework
        "21": [],  #  publications
        "107": [],  # responses-to-campaigns
        "22": "bulletins",  # revalidation-matters-bulletin
        "108": "blogs",  # roz-davies
        "23": "about-nhs-england",  # senior-team
        "109": "blogs",  # simon-bennett
        "110": "corporate-publications",  # special-advisers-gifts-hospitality-media
        "24": "bulletins",  # specialised-commissioning-stakeholder-bulletin
        "25": "statistics",
        "27": "statistics",  # statistics-information
        "29": [],  # the-month
        "111": "blogs",  # tim-kelsey
        "30": [],  # transition
        "31": "corporate-publications",  # transparency
        "32": [],  # twelve-months-on
        "1": [],  # uncategorized
        "34": "statistics",  # vte-risk-assessment-data-collection
        "35": "statistics",  # waiting-times-for-suspected-cancer-patients
        "36": "commissioning",  # whole-ccgs
        "39": "severe-weather-advice",  # winter-pressures-daily-situation-reports
        "37": "severe-weather-advice",  # winter-health-check-reports
        "38": "severe-weather-advice",  # winter-news-advice-and-blogs
        "1259": "commissioning",
        "1262": "integrated-care",
        "1261": [],  # public-health
        "1260": "commissioning",  # specialised-commissioning
        "26": "statistics",  # statistics-data-downloads
        "28": [],  # test
    },
    "categories-improvement-hub": {
        "2": "seven-day-services",  # 7-days-consistency-of-care
        "3": "urgent-and-emergency-care",  # acute-and-emergency-care
        "4": "cancer",
        "5": "nhs-workforce",  # capability-building
        "6": "cardiovascular",
        "7": [],  # care-planning
        "94": [],  # coffee-break
        "8": "community-and-social-care",  # community-services
        "9": "nhs-workforce",  # culture-and-leadership
        "10": ["elective-care", "training"],  # demand-and-capacity
        "11": "diabetes",  # diabetes-and-kidney-care
        "12": "statistics",  # diagnostics
        "13": "sustainability",  # efficiency-and-waste-reduction
        "14": "end-of-life-care",
        "15": "improvement",  # flow-and-improving-system-pathways
        "16": "improvement",  # improvement-tools
        "17": "innovation",
        "18": "integrated-care",
        "19": "improvement",  # large-scale-change
        "20": "older-people",  # living-longer-lives
        "21": "long-term-conditions",
        "22": "statistics",  # measurement
        "23": "mental-health",
        "93": "news",
        "25": "patient-safety",
        "24": "get-involved",  # patient-and-public-engagement
        "26": "primary-care",  # pimary-care
        "27": "respiratory",
        "95": [],  # spotlight
        "28": ["improvement", "innovation"],  # spread-and-adoption
        "29": "stroke",
        "30": "sustainability",
        "31": "improvement",  # system-transformation
        "1": [],  # uncategorized
    },
    "categories": {
        "3648": ["greener-nhs", "sustainability"],  # a-greener-nhs
        "21": "about-nhs-england",  # about-us
        "2595": "networks-and-collaboration",  # academic-health-science-network
        "2597": "governance-and-standards",  # accessible-information-standard
        "3561": ["ageing-well", "older-people"],  # ageing-well
        "2599": "allied-health-professionals",
        "2603": "corporate-publications",  # annual-report
        "2604": "armed-forces",
        "3741": "respiratory",  # asthma
        "2894": "integrated-care",  # better-care-fund
        "141": "corporate-publications",  # board-meetings
        "2610": "corporate-publications",  # business-plan
        "2523": "cancer",
        "2826": "carers",
        "2618": "children-and-young-people",
        "2832": "improvement",  # clinical-audit
        "2521": "commissioning",
        "3698": "coronavirus",
        "3595": "nhs-workforce",  # culture-and-leadership
        "2643": "dementia",
        "3754": "dentistry-and-oral-health",  # dental-care
        "2524": "diabetes",
        "2648": "digital",  # digital
        "3499": "emergency-preparedness-and-response",  # eu-exit
        "2884": "sustainability",  # efficiencies
        "2527": "elective-care",
        "2650": "emergency-preparedness-and-response",  # emergency-preparedness-resilience-and-response
        "2835": "end-of-life-care",
        "2651": "nhs-workforce",  # equality-and-diversity
        "3719": "estates-and-healthcare-properties",  # estates
        "2654": "events",
        "1672": "events",  # expo
        "2895": "optical",  # eye-health
        "2874": "finance",
        "2656": "corporate-publications",  # five-year-forward-view
        "3757": "nhs-workforce",  # flexible-working
        "3743": "respiratory",  # flu
        "1645": "statistics",  # friends-and-family-test
        "2565": ["online-services", "general-practice"],  # gp-online-services
        "3760": "public-health",  # gambling-addiction
        "2875": "gender-identity",
        "2560": "general-practice",
        "2659": "innovation",  # genomics
        "2687": "get-involved",
        "2827": "governance-and-standards",  # governance
        "2661": [],  # health-and-housing
        "2662": "health-and-justice",
        "3766": "healthcare-inequalities",
        "2878": [],  # healthcare-science
        "2665": "improvement",  # healthy-new-towns
        "2896": "hearing-loss",
        "2632": "cardiovascular",  # heart-disease
        "2041": "severe-weather-advice",  # hot-weather-news-and-advice
        "3758": "sexual-assault-and-abuse",  # identifying-and-responding-to-sexual-assault-and-abuse
        "2672": "governance-and-standards",  # information-standard
        "2671": "governance-and-standards",  # information-governance
        "2674": "innovation",
        "2679": "integrated-care",
        "2688": "integrated-care",  # lead-provider-framework
        "2298": "learning-disabilities",
        "2691": ["health-and-justice", "mental-health"],  # liaison-and-diversion
        "3444": "corporate-publications",  # long-term-plan
        "2502": "long-term-conditions",
        "2056": "maternity-midwifery-and-neonatal",  # maternity
        "2696": "pharmacy-and-medicine",  # medicine
        "2297": "mental-health",
        "3449": "long-term-conditions",  # musculoskeletal-conditions
        "2705": "nhs-111",
        "3677": "corporate-publications",  # nhs-birthday
        "3586": "improvement",  # nhs-improvement
        "3686": "nhs-workforce",  # nhs-people-plan
        "3687": "nhs-workforce",  # nhs-people-plan
        "2716": "improvement",  # nhs-rightcare
        "2717": "nhs-standard-contract",
        "2715": "finance",  # nhs-payment-system
        "3725": "nhs-providers",
        "3310": "corporate-publications",  # nhs70
        "3221": "governance-and-standards",  # national-quality-board
        "3730": "statistics",  # national-quarterly-pulse-survey
        "3235": "innovation",  # new-business-models
        "2245": "integrated-care",  # new-care-models
        "2735": [
            "nursing",
            "maternity-midwifery-and-neonatal",
        ],  # nursing-midwifery-and-care
        "2893": "obesity",
        "2718": "older-people",
        "3597": "statistics",  # operational-performance
        "2644": "dentistry-and-oral-health",  # oral-health
        "3562": "community-and-social-care",  # out-of-hospital-care
        "3752": [],  # outpatient-transformation-programme
        "2723": [],  # patient-care
        "1508": "patient-safety",
        "2729": "personalised-care",  # personal-health-budgets
        "2681": "personalised-care",
        "2731": "pharmacy-and-medicine",  # pharmacy
        "2732": "corporate-publications",  # planning-guidance
        "3563": [],  # prevention
        "2525": "primary-care",
        "2733": "commissioning",  # primary-care-co-commissioning
        "3593": "bulletins",  # provider-bulletin
        "3596": "improvement",  # quality-improvement
        "2877": "statistics",  # referral-to-treatment-times
        "2892": "respiratory",
        "2928": "primary-care",  # revalidation
        "2751": "safety",  # safe-staffing
        "2752": "safety",  # safeguarding
        "2755": "personalised-care",  # self-care
        "2756": [],  # sepsis
        "2757": "seven-day-services",
        "2666": "commissioning",  # specialised-commissioning
        "3769": "public-health",  # stop-smoking
        "3358": "stroke",
        "2512": "integrated-care",  # sustainability-and-transformation-partnerships
        "2764": "innovation",  # test-beds
        "2526": "urgent-and-emergency-care",
        "2771": "innovation",  # vanguards
        "2315": "get-involved",  # volunteering
        "2773": "personalised-care",  # wheelchair-services
        "2774": "safety",  # whistleblowing
        "1452": "severe-weather-advice",  # winter-news-and-advice
        "2876": "nhs-workforce",  # workforce
        "3771": "carers",  # young-carers
        "3775": "innovation", # nhs-accelerated-access-collaborative
        "3776": "statistics", # survey
    },
    "categories-aac": {
        "10": "innovation",  # artificial-intelligence
        "3": "innovation",  # nhs-accelerated-access-collaborative
        "4": "news",
        "1": [],  # uncategorized
    },
    "categories-rightcare": {
        "7": "blogs",
        "40": "improvement",  # nhs-rightcare
        "4": "news",
        "41": [],  # sepsis
    },
    "categories-coronavirus": {
        "4": "coronavirus",  # covid-19
        "3": "coronavirus",
        "2": "news",
        "1": [],  # uncategorized
    },
    "categories-greenernhs": {
        "9": "sustainability",  # net-zero
        "5": [],  # news-and-blogs
        "1": [],  # uncategorized
    },
    "categories-non-executive-opportunities": {
        "2": "corporate-publications",  # public-appointments
        "1": [],  # uncategorized
    },
    "regions": {
        "3367": "north-east",
        "3368": "north-west",
        "3369": "midlands",
        "3370": "central-and-east-of-england",
        "3371": "london",
        "3372": "south-east",
        "3373": "south-west",
    },
}
