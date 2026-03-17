"""
Centralized spam filters for job scraping.

Edit these lists to adjust filtering without touching the main script.
"""

# 🔴 SPAM KEYWORDS - Filter out jobs YOU'RE NOT ELIGIBLE FOR
# Based on your profile: Business Administration Major specializing in Accounting
# Targeting entry to mid-level roles in Toronto, Ontario, and Canada

SPAM_KEYWORDS = [
    # Seniority Levels (too senior / 10+ years required)
    "senior", "sr.", "sr ", "principal", "lead", "staff",
    "director", "head of", "vice president", "vp", "chief",
    "executive", "c-level", "distinguished", "fellow",

    # Experience Level Indicators
    "intermediate", "experienced professional",

    # Management/Leadership
    "manager", "mgr", "management", "supervisor", "team lead",

    # Irrelevant Tech Roles
    "software developer", "software engineer", "data scientist",
    "machine learning", "ml engineer", "ai engineer", "llm engineer",
    "devops", "site reliability", "infrastructure architect",
    "Java Developer", "Java", ".net",
    "database administrator", "dba", "system administrator",
    "network engineer", "telecommunications", "telecom",
    "quality assurance lead", "qa lead", "test lead",
    "Android", "Aerospace Engineer",

    # Architecture (typically 8+ years)
    "architect", "architecture lead", "solutions architect",
    "enterprise architect", "technical architect",

    # Engineering Disciplines (non-accounting)
    "civil engineer", "mechanical engineer", "electrical engineer",
    "fpga engineer", "hardware engineer", "embedded systems",
    "industrial engineer", "chemical engineer", "process engineer",
    "broadcast", "manufacturing science", "production engineer", "III",

    # Professional Designations Requiring Different Qualifications
    "p.eng", "p. eng", "professional engineer",
    "licensed professional", "registered engineer",

    # Security Clearance Required
    "secret clearance", "top secret", "security clearance required",
    "clearance eligible", "defense", "military clearance",

    # Language Requirements
    "bilingual french", "fluent french", "french required",
    "french mandatory", "bilinguisme", "bilingue",

    # Irrelevant Business / Non-Accounting Roles
    "product manager", "product management",
    "project manager", "program manager", "scrum master",
    "account manager", "sales", "marketing", "hr specialist",
    "people services", "recruitment", "talent acquisition",

    # Temporary / Commission / Unpaid Work
    "unpaid internship", "commission-based", "contractor only",

    # Predatory / Illegitimate Work Models
    "franchise", "mlm", "multi-level marketing", "sales-heavy",

    # Academic/Research (PhD required)
    "research scientist", "research lead", "postdoc", "post-doctoral",

    # Internships/Co-op (if you want full-time only)
    "intern", "internship", "co-op", "co op", "student position",
    "summer student", "coop", "stage", "stagiaire", "Consultant en Livraison",

    # Healthcare/Medical/Clinical
    "clinical", "healthcare practitioner", "medical", "pharmaceutical",
    "nursing", "therapy", "counseling",

    # Finance-Specific (requiring CFA/investment certifications)
    "portfolio manager", "investment analyst", "financial advisor",
    "wealth management",

    # Education/Teaching
    "professor", "instructor", "teacher", "tutor", "lecturer",
    "curriculum developer", "education specialist",

    # 🚫 Social / Mental Health / Support Roles
    "Crisis Responder", "Behaviour Analyst", "Social Worker", "Case Manager",
    "Occupational Therapist", "Speech Language Pathologist", "Audiologist",
    "Rehabilitation Specialist", "Mental Health Worker", "Addiction Counselor",
    "Therapeutic Support Staff", "Child and Youth Worker",
    "Early Childhood Educator", "Educational Assistant",
    "Special Education Teacher", "Learning Support Specialist",
    "Guidance Counselor", "Career Advisor", "Academic Advisor",
    "School Psychologist", "School Nurse",

    # 📚 Library / Museum / Heritage
    "Librarian", "Library Technician", "Archivist", "Museum Curator",
    "Conservation Technician", "Exhibit Designer", "Art Handler",
    "Gallery Manager", "Registrar", "Collections Manager",
    "Education Coordinator", "Public Programs Specialist",
    "Development Officer", "Fundraising Coordinator",
    "Grant Writer", "Donor Relations Manager", "Membership Coordinator",

    # 📣 Comms / Marketing / Media / Content
    "Communications Specialist", "Public Relations Officer",
    "Marketing Coordinator", "Social Media Manager",
    "Content Creator", "Copywriter", "Editor", "Proofreader",
    "Translator", "Interpreter", "Technical Writer", "Journalist",
    "Reporter", "News Anchor", "Broadcast Technician",
    "Camera Operator", "Sound Engineer", "Lighting Technician",
    "Video Producer", "Film Editor", "Production Assistant",
    "Video Editor", "Videographer",

    # 🎭 Creative / Arts / Production
    "Set Designer", "Costume Designer", "Makeup Artist",
    "Script Supervisor", "Location Scout", "Casting Director",
    "Talent Agent", "Art Director", "Creative Director",
    "Visual Effects Artist", "Animator", "Game Designer",

    # 🧠 Mental Health / Clinical Support
    "Psychotherapist", "Psychologist", "Counselor", "Counsellor",
    "Addictions Counselor", "Substance Use Counselor",
    "Caseworker", "Case Worker", "Support Worker",
    "Personal Support Worker", "PSW", "Residential Support Worker",
    "Shelter Worker", "Housing Support Worker", "Outreach Worker",
    "Community Support Worker", "Community Worker",
    "Family Support Worker", "Family Therapist",
    "Youth Counselor", "Youth Counsellor", "Youth Worker",
    "Child Protection Worker", "Crisis Intervention",
    "Crisis Support Worker", "Recreation Therapist",
    "Clinical Supervisor", "Clinical Coordinator",
    "Registered Nurse", "RN", "Registered Practical Nurse", "RPN",
    "Nurse Practitioner", "Nursing Assistant", "Health Care Aide",
    "Psychiatric Nurse", "Public Health Nurse",
    "Behaviour Therapist", "Rehabilitation Counselor",
    "Addiction Worker", "Mental Health Counselor",
    "Psychometrist",

    # 🎓 Education / School / Academic
    "Teacher", "Elementary Teacher", "High School Teacher",
    "Secondary Teacher", "College Instructor", "College Professor",
    "University Professor", "Faculty Member", "Lecturer",
    "Instructor", "Teaching Assistant",
    "Professor Emeritus", "Adjunct Professor",
    "Department Chair", "Vice Principal",
    "Dean", "School Administrator", "School Principal",
    "Education Assistant", "Instructional Coach",
    "Curriculum Specialist", "Learning Specialist",
    "Student Success Advisor", "Student Services Officer",
    "Residence Life Coordinator", "Residence Advisor",
    "Camp Counsellor", "Camp Counselor",

    # 🏛 Museum / Heritage (more)
    "Curatorial Assistant", "Curatorial Associate",
    "Curatorial Fellow", "Heritage Interpreter", "Heritage Officer",
    "Heritage Planner", "Museum Educator", "Museum Technician",
    "Collections Assistant", "Collections Technician",
    "Records Manager", "Records Technician", "Documentalist",
    "Archivist Assistant",

    # 🎯 Nonprofit / Fundraising / Events / Outreach
    "Development Coordinator", "Development Associate",
    "Development Manager", "Major Gifts Officer",
    "Philanthropy Officer", "Stewardship Officer",
    "Campaign Manager", "Campaign Coordinator",
    "Outreach Coordinator", "Community Engagement Coordinator",
    "Community Organizer", "Program Coordinator",
    "Program Facilitator", "Program Manager",
    "Event Coordinator", "Conference Coordinator",
    "Conference Planner", "Special Events Coordinator",
    "Volunteer Manager", "Volunteer Program Manager",

    # 📣 Comms / Brand / Marketing (more)
    "Communications Officer", "Communications Manager",
    "Communications Advisor", "Communications Consultant",
    "Brand Manager", "Brand Strategist",
    "Digital Marketing Specialist", "Digital Marketer",
    "SEO Specialist", "SEM Specialist",
    "Media Relations Officer", "Press Secretary",
    "Spokesperson", "Campaign Communications",
    "Public Affairs Specialist", "Public Information Officer",
    "Community Relations Coordinator",

    # 🎭 Theatre / Stage / Production Crew
    "Stage Manager", "Assistant Stage Manager",
    "Theatre Technician", "Theatre Manager",
    "Props Master", "Props Assistant",
    "Scenic Artist", "Storyboard Artist",
    "Storyboarder", "Sound Designer",
    "Foley Artist", "Post Production Supervisor",
    "Colorist", "Gaffer", "Best Boy",
    "Grip", "Production Designer",
    "Production Coordinator", "Production Manager",

    # 🏗️ Non-software Engineering (mechanical/civil/etc.)
    "Manufacturing Engineer", "Manufacturing Engineering",
    "Manufacturing Analyst", "Industrial Engineer",
    "Mechanical Systems Engineer", "Structural Engineer",
    "Geotechnical Engineer", "Mining Engineer", "Miner",
    "Rock Mechanics Engineer", "Hydraulic Engineer",
    "Hydraulics Engineer", "HVDC Engineer", "Power Engineer",
    "Substation Engineer", "Building Engineer",
    "HVAC Engineer", "HVAC Engineering",
    "Process Improvement Engineer", "Applied Dynamics Engineer",
    "Aviation Engineer", "Aircraft Structural", "Aircraft Dynamics",
    "Hydromechanical Engineer", "Airworthiness Engineer",
    "Thermodynamics Engineer", "Thermal Engineer", "Fluid Engineer",
    "Nuclear Operator", "Nuclear Engineer",
    "Microfluidics Engineer", "Stationary Engineer",
    "Conveyance Engineer",

    # 🛠 Trades / Technicians / Plant
    "Machining Specialist", "Assembler", "Assembly",
    "Valve Technician", "Robot Programmer", "Robotics Technician",
    "CNC", "Millwright", "Injection Molding",
    "Paint Technician", "Welding Specialist",
    "Quality Continuous Improvement Technician",
    "Transport Sustaining Engineer", "Shop Technician",
    "Machine Operator", "Operator",
    "Plant Technician", "Maintenance Technician",

    # 🧪 Lab / Wet-lab / Bio / Physical Sciences
    "Microbiologist", "Clinical Research",
    "Research Assistant (Physical Sciences)",
    "Lab Technician", "Scientist (wet lab)",
    "Biomedical", "Health Content Editor",

    # 🗂️ Admin / Office (non-technical)
    "Scheduling Coordinator", "Renewal Administrator",
    "Service Administrator", "Shop Administrator",
    "Office Administrator", "Housing Administrative",
    "Front Desk Agent",
    "Reporting Analyst (non-technical)",

    # ⚖️ Legal / Governance
    "Legal Counsel", "Lawyer", "Regulatory Affairs",
    "Governance",

    # 🎨 Generic non-tech design
    "Designer (non-UI)", "Motion Designer",
    "Graphic Designer", "Brand/UI Designer",

    # 🚚 Supply Chain / Logistics / Procurement
    "Supply Chain", "Procurement", "Logistics",
    "Operations Analyst (non-technical)",
    "Replenishment Analyst", "Vendor Analyst",

    # 🔐 Physical Security (not cyber)
    "Security Guard", "Guard", "Security Officer",

    # 👷 Misc unrelated jobs
    "Mechanic", "Bowling Mechanic",
    "Warehouse", "Factory", "Laborer",
    "Bartender", "Cook", "Driver", "compiler",
    "Field Technician", "Freelance",
    "Estimator", "Scheduler",
    "Paramedic", "Caregiver", "Patient Care",
]

# Additional spam/fake companies filter (matches `company` column)
SPAM_COMPANIES = [
    "Prime Jobs", "Next Jobs", "Jobs Ai", "Get Hired", "Crossover", "Recruit Loop", "Talent Pulse",
    "Get Jobs", "Jobsmast", "Hiring Hub", "Tech Jobs Fast", "YO IT CONSULTING", "DataAnnotation", "Mercor",
    "Talent Connect", "Recruit Loop", "Talent Orbit", "Talent Pulse", "S M Software Solutions Inc", "Lumenalta",
    "Crossing Hurdles", "Hire Sync", "Hire Wave", "HireFast", "Work Vista", "Hunter Bond", "Twine", "Talently",
    "Gnapi Technologies", "Peroptyx", "FutureSight", "HiJob.work", "jobbit", "Akkodis", 

    "EviSmart™", "Spait Infotech Private Limited", "Themesoft Inc.", "Mindrift", "Canonical", 
    "V-Soft Consulting Group, Inc.", "Compunnel Inc.", "Avanciers", "Avanciers Inc.", "Avancier's Inc.",  # covers all variations
    "Apexon", "Iris Software Inc.", "Galent", "n2psystems",
    "Resonaite", "Astra-North Infoteck Inc.", "Alimentiv", "Consultant en Livraison", 
    "Seven Hills Group Technologies Inc.", "Dexian", "DISYS",  # Dexian = former DISYS
    "Raas Infotek", "Kumaran Systems", "Luxoft", "Synechron",
    "Collabera", "Flexton Inc.", "Agilus Work Solutions",
    "Procom", "TEKsystems", "Robert Half", "Call For Referral",
    "Randstad Digital", "Randstad Digital Americas", "Next Match AI",
    "Hays", "Insight Global", "Andiamo", "Swoon", "Jerry", "CLEAResult", "micro1", "SOFTLINE TECHNOLOGY", ""
    "HCR Permanent Search", "Signature IT World Inc.",
    "Nexus Systems Group", "Altis Technology", "excelHR",
    "BeachHead", "Bevertec", "Robertson & Company Ltd.",        
]

# Dedicated spam keywords for description (phrases common in spammy descriptions)
SPAM_DESCRIPTION_KEYWORDS = [
    "quick money", "5+ years", "6+ years", "7+ years", "8+ years", "10+ years",
    "9 years", "6 years", "7 years", "8 years",
    "10+ years experience", "commission only", "unpaid internship",
    "multi-level marketing", "franchise opportunity",
]
