SITE_INFO = {
    "name": "Vishwajit Parmar",
    "title": "Python / Odoo Developer",
    "email": "vishwajit25401@gmail.com",
    "phone": "+91-7573827190",
    "location": "Vadodara, Gujarat",
    "summary": (
        "Results-driven Python/Odoo Developer with 3+ years of hands-on experience "
        "in designing, developing, and implementing scalable ERP solutions. Proven "
        "expertise in customizing Odoo modules, optimizing business workflows, and "
        "delivering high-quality solutions aligned with client requirements."
    ),
    "github": "https://github.com/visu-25",
    "linkedin": "https://www.linkedin.com/in/vishwajit-parmar-4106b3248",
}


def site_info(request):
    return {"site": SITE_INFO}
