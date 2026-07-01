# DevBook – Developer Portfolio & Project Registry

DevBook is a lightweight, responsive mini-platform designed for peer developer networks, classes, or bootcamps to aggregate and display their programming projects in one central hub. Instead of hosting an isolated portfolio, users can sign up, create a developer profile, attach their backend validation certificates, and securely register their web apps with active deployment links and technology tags.

The system features a centralized, searchable global dashboard that allows recruiters or peers to instantly filter down project cards using real-time client-side scripting.

---

## 🛠️ Tech Stack & Architecture

- **Backend Framework:** Django 5.x (Python)
- **Database Engine:** MySQL (Relational management utilizing Foreign Keys and Cascading deletes)
- **Frontend Presentation:** Semantic HTML5, Custom CSS3 Grid/Cards layout
- **Client-Side Scripting:** Vanilla JavaScript (Asynchronous Event Listeners for DOM manipulation)

---

## ✨ Key Features

- **Secure User Authentication System:** Built using Django’s security layer to handle clean User Signups, Logins, and Logout actions.
- **Extended Profile Tables:** Uses Django database signals to generate a developer `Profile` automatically upon signup, allowing users to showcase their LinkedIn profiles and Backend Certificates.
- **Strict Row-Level CRUD Security:** Full Create, Read, Update, and Delete capabilities on project listings. Users maintain total visibility over the registry but are strictly locked out from modifying or deleting entries owned by other developers.
- **Instant JavaScript Search Filter:** A fast frontend filter script that scans the dataset parameters in the DOM to hide or reveal project cards instantly based on matching technology tags (e.g., *Django, PostgreSQL, JavaScript*) without generating database hits or page refreshes.

---

## 📊 Database Schema (PostgreSQL Architecture)

The system leverages a relational model structured cleanly across three interconnected tables:

1. **auth_user (Built-in):** Manages essential security credentials (`id`, `username`, `email`, hashed `password`).
2. **projects_profile (1:1 Relationship):** Maps data fields directly to the user record (`bio`, `linkedin_url`, `certificate_url`) via a `OneToOneField`.
3. **projects_project (1:N Relationship):** Links multiple engineering projects to an individual account using a `ForeignKey` constraint with `on_delete=models.CASCADE`.

---

## 🚀 Installation & Local Deployment

### 1. Prerequisites
Ensure you have Python 3.x installed and a local MySQL server instance running.

### 2. Clone the Repository
```bash
git clone [https://github.com/codewithmittalhardik/portfolio.git](https://github.com/codewithmittalhardik/portfolio.git)
cd portfolio