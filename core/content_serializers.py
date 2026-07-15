from core.content_defaults import DEFAULT_PERSONA, DEFAULT_PHILOSOPHY, DEFAULT_SKILLS
from core.models import PersonaSection, PhilosophyParagraph, TechnicalSkill


def serialize_persona(persona: PersonaSection) -> dict:
    return {
        "id": persona.id,
        "heading": persona.heading,
        "description": persona.description,
        "image_role_label": persona.image_role_label,
    }


def serialize_philosophy(paragraph: PhilosophyParagraph) -> dict:
    return {
        "id": paragraph.id,
        "order": paragraph.order,
        "content": paragraph.content,
        "is_active": paragraph.is_active,
    }


def serialize_skill(skill: TechnicalSkill) -> dict:
    return {
        "id": skill.id,
        "order": skill.order,
        "skill_id": skill.skill_id,
        "title": skill.title,
        "subtitle": skill.subtitle,
        "proficiency": skill.proficiency,
        "color": skill.color,
        "icon": skill.icon,
        "tags": skill.tags,
        "is_active": skill.is_active,
    }


def default_persona_payload() -> dict:
    return dict(DEFAULT_PERSONA)


def default_philosophy_payload() -> list[dict]:
    return [
        {"id": None, "order": index + 1, "content": content, "is_active": True}
        for index, content in enumerate(DEFAULT_PHILOSOPHY)
    ]


def default_skills_payload() -> list[dict]:
    return [
        {
            "id": None,
            "order": skill["order"],
            "skill_id": skill["skill_id"],
            "title": skill["title"],
            "subtitle": skill["subtitle"],
            "proficiency": skill["proficiency"],
            "color": skill["color"],
            "icon": skill["icon"],
            "tags": skill["tags"],
            "is_active": True,
        }
        for skill in DEFAULT_SKILLS
    ]


def get_public_home_content() -> dict:
    persona = PersonaSection.objects.first()
    philosophy = PhilosophyParagraph.objects.filter(is_active=True)
    skills = TechnicalSkill.objects.filter(is_active=True)

    return {
        "persona": serialize_persona(persona) if persona else default_persona_payload(),
        "philosophy": [serialize_philosophy(item) for item in philosophy]
        or default_philosophy_payload(),
        "skills": [serialize_skill(item) for item in skills] or default_skills_payload(),
    }
