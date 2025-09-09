from django.core.files.base import ContentFile
from django.utils import timezone
from apps.jobs.models import JobPosting
from apps.jobs.scoring import upsert_score
from apps.core.models import Document
from .models import Application


def tailor_cover_letter(user, job: JobPosting, tone: str = "professional") -> Document:
    ms = upsert_score(job, user)
    overlap = ms.features.get("overlap", []) if isinstance(ms.features, dict) else []
    text = f"""
    Dear Hiring Team,

    I’m excited to apply for the {job.title} role at {job.company.name if job.company else 'your company'}. My experience aligns with your needs, and I bring strengths in {', '.join(overlap[:8]) or 'relevant skills'}.

    Highlights:
    - Impactful work in similar domains.
    - Strong collaboration and ownership.
    - Continuous learning and pragmatic problem-solving.

    I would welcome a chance to discuss how I can contribute to the team.

    Best regards,
    {user.get_username()}
    """.strip()

    content = ContentFile(text.encode("utf-8"))
    title = f"Cover - {job.title} - {timezone.now().date()}"
    doc = Document.objects.create(owner=user, kind="cover_letter", title=title)
    doc.file.save(f"cover_{job.id}.txt", content, save=True)
    doc.metadata = {"job_id": job.id, "tone": tone, "features": ms.features}
    doc.save(update_fields=["metadata", "updated_at"])
    return doc


def attach_documents_to_application(app: Application, resume_id: int | None = None, cover_id: int | None = None) -> Application:
    changed = False
    if resume_id and app.resume_id != resume_id:
        app.resume_id = resume_id
        changed = True
    if cover_id and app.cover_letter_id != cover_id:
        app.cover_letter_id = cover_id
        changed = True
    if changed:
        app.save(update_fields=["resume", "cover_letter", "updated_at"])
    return app


def tailor_resume(user, job: JobPosting) -> Document:
    ms = upsert_score(job, user)
    overlap = ms.features.get("overlap", []) if isinstance(ms.features, dict) else []
    bullets = '\n'.join([f"- Experience with {k}" for k in overlap[:10]]) or "- Relevant experience matching role requirements"
    text = f"""
    {user.get_username()}
    Summary: Skilled professional aligning with {job.title}. Key strengths include {', '.join(overlap[:6]) or 'relevant technologies'}.

    Highlights:
    {bullets}

    Experience:
    - Company A — Role (YYYY–YYYY)
      Impact: Quantified achievement.
    - Company B — Role (YYYY–YYYY)
      Impact: Quantified achievement.

    Education & Certifications
    - ...
    """.strip()

    content = ContentFile(text.encode('utf-8'))
    title = f"Resume - {job.title} - {timezone.now().date()}"
    doc = Document.objects.create(owner=user, kind="resume", title=title)
    doc.file.save(f"resume_{job.id}.txt", content, save=True)
    doc.metadata = {"job_id": job.id, "features": ms.features, "tailored": True}
    doc.save(update_fields=["metadata", "updated_at"])
    return doc
