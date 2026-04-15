from __future__ import annotations

import argparse
from datetime import date, datetime, timezone
from pathlib import Path
import re

POSTS_DIR = Path("_posts")
DEFAULT_START_DATE = date(2026, 4, 15)

GERMAN_CHAR_MAP = {
    "ä": "ae",
    "ö": "oe",
    "ü": "ue",
    "ß": "ss",
}

falowen30DayBlogCalendar = {
  "day_1": {
    "title": "Why Learning German in Ghana Is a Smart Move",
    "slug": "why-learning-german-in-ghana-is-a-smart-move",
    "keyword": "learn German in Ghana",
    "category": "German Learning",
    "excerpt": "Discover how learning German in Ghana can open doors to study, work, and international opportunities.",
    "focus": "Benefits of learning German for study, work, and travel",
    "promotion_angle": "Show how Falowen and Learn Language Education Academy make German accessible",
    "cta": "Register now at Learn Language Education Academy and start learning German with Falowen.",
    "unsplash_link": "https://unsplash.com/s/photos/student-studying-laptop",
    "meta_title": "Learn German in Ghana | Start with Falowen",
    "meta_description": "Learn why studying German in Ghana is a smart move for education, work, and travel. Join Learn Language Education Academy with Falowen."
  },
  "day_2": {
    "title": "German Alphabet for Complete Beginners",
    "slug": "german-alphabet-for-complete-beginners",
    "keyword": "German alphabet for beginners",
    "category": "Beginner German",
    "excerpt": "Learn the German alphabet in a simple way and build a strong foundation for speaking and reading.",
    "focus": "Teach German letters and pronunciation basics",
    "promotion_angle": "Position Falowen as an easy starting point for beginners",
    "cta": "Start your beginner German journey today with Falowen and our guided classes.",
    "unsplash_link": "https://unsplash.com/s/photos/alphabet-letters",
    "meta_title": "German Alphabet for Beginners | Falowen",
    "meta_description": "Master the German alphabet with easy beginner lessons. Start learning German step by step with Falowen."
  },
  "day_3": {
    "title": "10 German Greetings You Can Use Every Day",
    "slug": "10-german-greetings-you-can-use-every-day",
    "keyword": "German greetings",
    "category": "German Vocabulary",
    "excerpt": "Learn 10 useful German greetings you can use daily in class, at work, and in conversations.",
    "focus": "Common greetings like Hallo, Guten Morgen, and Guten Abend",
    "promotion_angle": "Encourage daily speaking practice through Falowen lessons",
    "cta": "Join our German classes and practice real-life greetings with confidence.",
    "unsplash_link": "https://unsplash.com/s/photos/people-greeting",
    "meta_title": "10 German Greetings for Beginners",
    "meta_description": "Learn common German greetings for daily conversation. Practice speaking with Falowen and Learn Language Education Academy."
  },
  "day_4": {
    "title": "How to Introduce Yourself in German",
    "slug": "how-to-introduce-yourself-in-german",
    "keyword": "introduce yourself in German",
    "category": "Speaking Practice",
    "excerpt": "Learn simple sentences to introduce yourself in German with confidence as a beginner.",
    "focus": "Simple self-introduction sentences",
    "promotion_angle": "Show that students can speak from their first lessons",
    "cta": "Enroll now and start speaking German from your first lesson.",
    "unsplash_link": "https://unsplash.com/s/photos/portrait-speaking",
    "meta_title": "How to Introduce Yourself in German",
    "meta_description": "Learn how to introduce yourself in German with simple examples for beginners. Start speaking with Falowen today."
  },
  "day_5": {
    "title": "20 Basic German Words Every Student Must Know",
    "slug": "20-basic-german-words-every-student-must-know",
    "keyword": "basic German words",
    "category": "German Vocabulary",
    "excerpt": "Build your vocabulary with 20 basic German words every beginner should know.",
    "focus": "Important beginner vocabulary",
    "promotion_angle": "Promote Falowen as a step-by-step vocabulary builder",
    "cta": "Build your German vocabulary faster with Falowen and our classes.",
    "unsplash_link": "https://unsplash.com/s/photos/notebook-vocabulary",
    "meta_title": "20 Basic German Words for Beginners",
    "meta_description": "Learn 20 essential German words every beginner should know. Study vocabulary the easy way with Falowen."
  },
  "day_6": {
    "title": "How Falowen Helps You Learn German Faster",
    "slug": "how-falowen-helps-you-learn-german-faster",
    "keyword": "learn German with Falowen",
    "category": "Falowen",
    "excerpt": "See how Falowen supports students with flexible lessons, guided practice, and easy learning tools.",
    "focus": "Explain Falowen features and learning support",
    "promotion_angle": "Direct product promotion",
    "cta": "Sign up today and start learning German with Falowen.",
    "unsplash_link": "https://unsplash.com/s/photos/education-app-phone",
    "meta_title": "Learn German Faster with Falowen",
    "meta_description": "Discover how Falowen helps students learn German faster through guided lessons and flexible study support."
  },
  "day_7": {
    "title": "German Numbers 1 to 20 Made Easy",
    "slug": "german-numbers-1-to-20-made-easy",
    "keyword": "German numbers 1 to 20",
    "category": "Beginner German",
    "excerpt": "Learn German numbers from 1 to 20 in a simple and practical way for beginners.",
    "focus": "Teach numbers with examples",
    "promotion_angle": "Show simple practical learning methods",
    "cta": "Join our beginner classes for more simple German lessons.",
    "unsplash_link": "https://unsplash.com/s/photos/numbers-classroom",
    "meta_title": "German Numbers 1 to 20 for Beginners",
    "meta_description": "Learn German numbers 1 to 20 with simple examples and easy practice. Start your beginner lessons with Falowen."
  },
  "day_8": {
    "title": "Days of the Week in German",
    "slug": "days-of-the-week-in-german",
    "keyword": "days of the week in German",
    "category": "German Vocabulary",
    "excerpt": "Learn the days of the week in German and how to use them in daily conversation.",
    "focus": "Teach weekdays and how to use them in sentences",
    "promotion_angle": "Promote learning through everyday conversation topics",
    "cta": "Learn practical German today with Learn Language Education Academy.",
    "unsplash_link": "https://unsplash.com/s/photos/calendar-planner",
    "meta_title": "Days of the Week in German",
    "meta_description": "Learn the days of the week in German with simple examples for beginners. Practice practical German with Falowen."
  },
  "day_9": {
    "title": "How to Tell the Time in German",
    "slug": "how-to-tell-the-time-in-german",
    "keyword": "tell the time in German",
    "category": "Beginner German",
    "excerpt": "Master basic time expressions in German and start using them in everyday conversations.",
    "focus": "Basic time expressions",
    "promotion_angle": "Highlight useful real-life German",
    "cta": "Master everyday German by joining our guided program today.",
    "unsplash_link": "https://unsplash.com/s/photos/clock-time",
    "meta_title": "How to Tell the Time in German",
    "meta_description": "Learn how to tell the time in German with easy examples and beginner-friendly explanations. Study practical German with Falowen."
  },
  "day_10": {
    "title": "Simple German Sentences You Can Start Using Today",
    "slug": "simple-german-sentences-you-can-start-using-today",
    "keyword": "simple German sentences",
    "category": "Speaking Practice",
    "excerpt": "Learn simple German sentence patterns you can start using right away as a beginner.",
    "focus": "Basic sentence patterns",
    "promotion_angle": "Show fast progress through structured lessons",
    "cta": "Begin your German speaking journey with our classes today.",
    "unsplash_link": "https://unsplash.com/s/photos/writing-notebook",
    "meta_title": "Simple German Sentences for Beginners",
    "meta_description": "Start using simple German sentences today. Learn beginner sentence patterns with Falowen and Learn Language Education Academy."
  },
  "day_11": {
    "title": "Why Students Love Learn Language Education Academy",
    "slug": "why-students-love-learn-language-education-academy",
    "keyword": "German classes in Ghana",
    "category": "Academy",
    "excerpt": "Find out why students choose Learn Language Education Academy for practical and flexible German lessons.",
    "focus": "Talk about teaching style, flexibility, and support",
    "promotion_angle": "Promote academy value and trust",
    "cta": "Register now and become one of our successful German students.",
    "unsplash_link": "https://unsplash.com/s/photos/happy-students-classroom",
    "meta_title": "German Classes in Ghana | Learn Language Education Academy",
    "meta_description": "See why students love Learn Language Education Academy for German lessons in Ghana. Join our flexible classes with Falowen."
  },
  "day_12": {
    "title": "Der, Die, Das Explained Simply",
    "slug": "der-die-das-explained-simply",
    "keyword": "der die das explained",
    "category": "German Grammar",
    "excerpt": "Learn how der, die, and das work in German with simple explanations for beginners.",
    "focus": "Teach German articles in a beginner-friendly way",
    "promotion_angle": "Show that even difficult topics can be made easy with Falowen",
    "cta": "Learn German grammar the easy way by joining our classes.",
    "unsplash_link": "https://unsplash.com/s/photos/grammar-book",
    "meta_title": "Der Die Das Explained for Beginners",
    "meta_description": "Understand der, die, and das with easy German grammar lessons for beginners. Study clearly with Falowen."
  },
  "day_13": {
    "title": "Top 10 German Verbs for Beginners",
    "slug": "top-10-german-verbs-for-beginners",
    "keyword": "German verbs for beginners",
    "category": "German Vocabulary",
    "excerpt": "Learn 10 important German verbs every beginner needs for daily conversation.",
    "focus": "Teach useful verbs like sein, haben, gehen, and machen",
    "promotion_angle": "Promote practical learning",
    "cta": "Study useful German verbs with our guided lessons today.",
    "unsplash_link": "https://unsplash.com/s/photos/language-textbook",
    "meta_title": "Top 10 German Verbs for Beginners",
    "meta_description": "Learn the most useful German verbs for beginners and improve your daily conversation skills with Falowen."
  },
  "day_14": {
    "title": "How to Talk About Your Family in German",
    "slug": "how-to-talk-about-your-family-in-german",
    "keyword": "family in German",
    "category": "Speaking Practice",
    "excerpt": "Learn family vocabulary and simple sentences to talk about your family in German.",
    "focus": "Family vocabulary and sentence examples",
    "promotion_angle": "Show relatable conversation practice",
    "cta": "Join our classes and learn to speak naturally in German.",
    "unsplash_link": "https://unsplash.com/s/photos/family-home",
    "meta_title": "How to Talk About Family in German",
    "meta_description": "Learn how to talk about your family in German with easy vocabulary and simple beginner examples."
  },
  "day_15": {
    "title": "German Words for the Classroom",
    "slug": "german-words-for-the-classroom",
    "keyword": "German classroom words",
    "category": "German Vocabulary",
    "excerpt": "Learn useful German classroom words that students can use every day in lessons.",
    "focus": "Teach school and classroom vocabulary",
    "promotion_angle": "Connect learning to student life",
    "cta": "Start learning German with a system that works for students.",
    "unsplash_link": "https://unsplash.com/s/photos/classroom-books",
    "meta_title": "German Classroom Words for Beginners",
    "meta_description": "Learn common German classroom words and phrases for daily lessons. Study step by step with Falowen."
  },
  "day_16": {
    "title": "How to Ask Simple Questions in German",
    "slug": "how-to-ask-simple-questions-in-german",
    "keyword": "German question words",
    "category": "Speaking Practice",
    "excerpt": "Learn how to ask simple questions in German using common question words.",
    "focus": "Question words like wo, was, wer, wann",
    "promotion_angle": "Highlight speaking confidence",
    "cta": "Build your confidence in German by joining our classes today.",
    "unsplash_link": "https://unsplash.com/s/photos/student-raising-hand",
    "meta_title": "How to Ask Questions in German",
    "meta_description": "Learn German question words and how to ask simple questions in everyday conversation. Practice with Falowen."
  },
  "day_17": {
    "title": "German for Shopping: Useful Words and Phrases",
    "slug": "german-for-shopping-useful-words-and-phrases",
    "keyword": "German shopping phrases",
    "category": "German Vocabulary",
    "excerpt": "Learn useful German shopping words and phrases for real-life situations.",
    "focus": "Teach shopping vocabulary and dialogues",
    "promotion_angle": "Promote real-life communication practice",
    "cta": "Learn real-world German today with Falowen and our classes.",
    "unsplash_link": "https://unsplash.com/s/photos/shopping-market",
    "meta_title": "German for Shopping | Beginner Phrases",
    "meta_description": "Learn German shopping vocabulary and phrases for everyday use. Practice practical German with Falowen."
  },
  "day_18": {
    "title": "Learn German Online from Anywhere",
    "slug": "learn-german-online-from-anywhere",
    "keyword": "learn German online",
    "category": "Falowen",
    "excerpt": "Study German online from anywhere with flexible lessons and guided support.",
    "focus": "Benefits of flexible online learning",
    "promotion_angle": "Promote Falowen convenience and accessibility",
    "cta": "Study from anywhere by joining Falowen today.",
    "unsplash_link": "https://unsplash.com/s/photos/online-learning-laptop",
    "meta_title": "Learn German Online with Falowen",
    "meta_description": "Learn German online from anywhere with flexible lessons and guided support from Falowen and Learn Language Education Academy."
  },
  "day_19": {
    "title": "Common German Pronunciation Tips for Beginners",
    "slug": "common-german-pronunciation-tips-for-beginners",
    "keyword": "German pronunciation tips",
    "category": "Pronunciation",
    "excerpt": "Improve your German speaking with easy pronunciation tips for common sounds.",
    "focus": "Teach sounds like ch, sch, ei, ie",
    "promotion_angle": "Position academy as helpful for speaking improvement",
    "cta": "Improve your pronunciation with our guided German support.",
    "unsplash_link": "https://unsplash.com/s/photos/headset-speaking",
    "meta_title": "German Pronunciation Tips for Beginners",
    "meta_description": "Learn common German pronunciation tips for beginners and improve your speaking with simple practice."
  },
  "day_20": {
    "title": "How to Describe Your Daily Routine in German",
    "slug": "how-to-describe-your-daily-routine-in-german",
    "keyword": "daily routine in German",
    "category": "Speaking Practice",
    "excerpt": "Learn useful verbs and sentence structures to describe your daily routine in German.",
    "focus": "Useful verbs and sentence structures",
    "promotion_angle": "Show how students move into real communication",
    "cta": "Take the next step in German with our practical classes.",
    "unsplash_link": "https://unsplash.com/s/photos/morning-routine-desk",
    "meta_title": "How to Talk About Daily Routine in German",
    "meta_description": "Learn how to describe your daily routine in German with easy verbs and sentence patterns for beginners."
  },
  "day_21": {
    "title": "5 Mistakes Beginners Make When Learning German",
    "slug": "5-mistakes-beginners-make-when-learning-german",
    "keyword": "German learning mistakes",
    "category": "German Learning",
    "excerpt": "Avoid the most common mistakes beginners make when learning German and improve faster.",
    "focus": "Common learning mistakes and how to avoid them",
    "promotion_angle": "Promote expert guidance from the academy",
    "cta": "Learn the right way with Learn Language Education Academy.",
    "unsplash_link": "https://unsplash.com/s/photos/confused-student",
    "meta_title": "5 Common German Learning Mistakes",
    "meta_description": "Discover the top mistakes beginners make when learning German and how to avoid them with better guidance."
  },
  "day_22": {
    "title": "How German Can Help You Study Abroad",
    "slug": "how-german-can-help-you-study-abroad",
    "keyword": "study abroad in Germany",
    "category": "Opportunities",
    "excerpt": "See how learning German can support your dream of studying abroad in Germany.",
    "focus": "German for education opportunities",
    "promotion_angle": "Promote the long-term value of learning German",
    "cta": "Start preparing for your future with German today.",
    "unsplash_link": "https://unsplash.com/s/photos/university-student",
    "meta_title": "How German Helps You Study Abroad",
    "meta_description": "Learn how German language skills can help you study abroad and access more international opportunities."
  },
  "day_23": {
    "title": "German Vocabulary for Travel",
    "slug": "german-vocabulary-for-travel",
    "keyword": "German travel vocabulary",
    "category": "German Vocabulary",
    "excerpt": "Learn useful German travel words and phrases for airports, hotels, and everyday travel situations.",
    "focus": "Useful travel-related words and phrases",
    "promotion_angle": "Show practical uses of German",
    "cta": "Learn useful German for travel, study, and work with us.",
    "unsplash_link": "https://unsplash.com/s/photos/travel-suitcase-airport",
    "meta_title": "German Vocabulary for Travel",
    "meta_description": "Learn German travel vocabulary and phrases for real-life use. Study practical German with Falowen."
  },
  "day_24": {
    "title": "How to Write a Simple Email in German",
    "slug": "how-to-write-a-simple-email-in-german",
    "keyword": "write email in German",
    "category": "Writing Skills",
    "excerpt": "Learn how to write a simple email in German with beginner-friendly structure and examples.",
    "focus": "Basic writing structure and examples",
    "promotion_angle": "Promote academic and professional writing support",
    "cta": "Build your German writing skills with our guided lessons.",
    "unsplash_link": "https://unsplash.com/s/photos/laptop-email",
    "meta_title": "How to Write an Email in German",
    "meta_description": "Learn how to write a simple email in German with easy examples for beginners. Improve your writing with Falowen."
  },
  "day_25": {
    "title": "Why Daily Practice Matters in Learning German",
    "slug": "why-daily-practice-matters-in-learning-german",
    "keyword": "daily German practice",
    "category": "German Learning",
    "excerpt": "Discover why daily practice is one of the best ways to improve your German faster.",
    "focus": "Encourage consistency and study habits",
    "promotion_angle": "Promote Falowen as a daily learning companion",
    "cta": "Stay consistent by learning with Falowen every day.",
    "unsplash_link": "https://unsplash.com/s/photos/habit-tracker-journal",
    "meta_title": "Why Daily German Practice Matters",
    "meta_description": "Learn why daily German practice is important for steady progress and how Falowen helps you stay consistent."
  },
  "day_26": {
    "title": "How Falowen Supports Your German Learning Journey",
    "slug": "how-falowen-supports-your-german-learning-journey",
    "keyword": "Falowen German learning",
    "category": "Falowen",
    "excerpt": "See how Falowen supports your progress with lessons, practice tools, and flexible learning.",
    "focus": "Explain app-based learning, lessons, and progress",
    "promotion_angle": "Brand promotion with student benefit",
    "cta": "Sign up now and grow your German with Falowen.",
    "unsplash_link": "https://unsplash.com/s/photos/mobile-app-dashboard",
    "meta_title": "Falowen for German Learning",
    "meta_description": "Discover how Falowen supports your German learning journey with flexible study tools and guided lessons."
  },
  "day_27": {
    "title": "German Sentence Structure for Beginners",
    "slug": "german-sentence-structure-for-beginners",
    "keyword": "German sentence structure",
    "category": "German Grammar",
    "excerpt": "Learn the basics of German sentence structure in a simple and beginner-friendly way.",
    "focus": "Basic word order in simple sentences",
    "promotion_angle": "Show that grammar can be taught clearly",
    "cta": "Learn German grammar step by step with our classes.",
    "unsplash_link": "https://unsplash.com/s/photos/chalkboard-grammar",
    "meta_title": "German Sentence Structure for Beginners",
    "meta_description": "Understand basic German sentence structure with simple examples and beginner-friendly explanations."
  },
  "day_28": {
    "title": "How to Talk About Your Hobbies in German",
    "slug": "how-to-talk-about-your-hobbies-in-german",
    "keyword": "hobbies in German",
    "category": "Speaking Practice",
    "excerpt": "Learn how to talk about your hobbies in German using simple words and sentence examples.",
    "focus": "Teach hobby-related vocabulary and examples",
    "promotion_angle": "Promote fun and personal communication",
    "cta": "Join our classes and start expressing yourself in German.",
    "unsplash_link": "https://unsplash.com/s/photos/hobby-reading-music-sports",
    "meta_title": "How to Talk About Hobbies in German",
    "meta_description": "Learn how to talk about your hobbies in German with easy vocabulary and speaking examples for beginners."
  },
  "day_29": {
    "title": "Why This Is the Best Time to Start Learning German",
    "slug": "why-this-is-the-best-time-to-start-learning-german",
    "keyword": "start learning German",
    "category": "Academy",
    "excerpt": "See why now is the best time to start learning German and take the first step toward your goals.",
    "focus": "Motivation and urgency",
    "promotion_angle": "Encourage immediate sign-up",
    "cta": "Register today at Learn Language Education Academy.",
    "unsplash_link": "https://unsplash.com/s/photos/motivated-student-desk",
    "meta_title": "Start Learning German Today",
    "meta_description": "Find out why now is the best time to start learning German and join Learn Language Education Academy with Falowen."
  },
  "day_30": {
    "title": "How to Join Learn Language Education Academy and Start Learning German",
    "slug": "how-to-join-learn-language-education-academy-and-start-learning-german",
    "keyword": "join German classes",
    "category": "Academy",
    "excerpt": "Learn how to join Learn Language Education Academy and begin your German journey with Falowen.",
    "focus": "Clear guide on how to sign up",
    "promotion_angle": "Direct conversion post",
    "cta": "Sign up now and begin your German journey with Falowen.",
    "unsplash_link": "https://unsplash.com/s/photos/signup-laptop",
    "meta_title": "Join German Classes | Learn Language Education Academy",
    "meta_description": "Ready to learn German? Join Learn Language Education Academy and start your journey with Falowen today."
  }
}

DAILY_MESSAGE_VARIATIONS = [
    "Today, choose one tiny action and complete it before the day ends.",
    "Repeat this lesson out loud three times to make it stick.",
    "Write one mini paragraph and share it with a classmate for feedback.",
    "Use this topic in a voice note so you hear your own progress.",
    "Set a 10-minute timer and focus only on this learning goal.",
    "Turn today's concept into a simple real-life conversation.",
    "Add these words to your personal revision notebook today.",
    "Practice this lesson at the same time tomorrow to build consistency.",
    "Challenge yourself to use this topic in two different sentence patterns.",
    "Read your examples slowly, then faster, for natural fluency.",
    "Pair this lesson with yesterday's topic to build stronger memory links.",
    "Focus on accuracy first, then speed, for better long-term results.",
    "Teach one point from this lesson to someone else today.",
    "Keep your examples personal so they are easier to remember.",
    "Record one mistake you made and rewrite it correctly three times.",
    "Use this lesson in chat and in speaking so both skills improve.",
    "Try this topic in a market, class, or social scenario this week.",
    "Review your old notes and connect them to today's new concept.",
    "Create a five-line routine around this lesson for daily practice.",
    "Practice with confidence; simple language used correctly is powerful.",
    "Revisit this post tonight and test yourself without looking at notes.",
    "Build one question and one answer from today's keyword.",
    "Use this topic to role-play a practical German conversation.",
    "Add today's key phrase to your email or writing practice.",
    "Stack this lesson with pronunciation practice for stronger output.",
    "Track your streak: one lesson each day for visible progress.",
    "Summarize today's lesson in your own words before you sleep.",
    "Practice this concept in both formal and casual German.",
    "Set a weekly goal and use today's lesson as your starting point.",
    "Celebrate your consistency—small wins create fluent speakers.",
]

BASE_FALOWEN_ANGLE = (
    "Falowen is a German learning app built by Ghanaians to help students progress faster. "
    "It combines AI learning tools, a built syllabus, structured assignments, and a progress tracker "
    "that has helped many students prepare for and pass their Goethe exams."
)

CONTENT_TYPE_BY_DAY = {
    1: "promo_essay",
    2: "grammar_notes",
    3: "vocabulary_notes",
    4: "how_to_guide",
    5: "vocabulary_notes",
    6: "promo_essay",
    7: "vocabulary_notes",
    8: "vocabulary_notes",
    9: "grammar_notes",
    10: "grammar_notes",
    11: "promo_essay",
    12: "grammar_notes",
    13: "grammar_notes",
    14: "how_to_guide",
    15: "vocabulary_notes",
    16: "grammar_notes",
    17: "vocabulary_notes",
    18: "promo_essay",
    19: "grammar_notes",
    20: "how_to_guide",
    21: "list_post",
    22: "promo_essay",
    23: "vocabulary_notes",
    24: "how_to_guide",
    25: "promo_essay",
    26: "promo_essay",
    27: "grammar_notes",
    28: "how_to_guide",
    29: "promo_essay",
    30: "promo_essay",
}


def slugify(text: str) -> str:
    text = text.strip().lower()
    for src, target in GERMAN_CHAR_MAP.items():
        text = text.replace(src, target)
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return (text[:90].strip("-") or "post")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate one daily blog post from a fixed 30-day calendar.")
    parser.add_argument("--date", help="Publishing date in YYYY-MM-DD format (default: current UTC date).")
    parser.add_argument("--start-date", help="Start date for day_1 in YYYY-MM-DD format (default: 2026-04-15).")
    parser.add_argument("--force", action="store_true", help="Overwrite existing file if present.")
    parser.add_argument("--dry-run", action="store_true", help="Print what would happen without writing file.")
    return parser.parse_args()


def resolve_date(raw_date: str | None, fallback: date | None = None) -> date:
    if raw_date:
        return datetime.strptime(raw_date, "%Y-%m-%d").date()
    return fallback or datetime.now(timezone.utc).date()


def compute_day_number(run_date: date, start_date: date) -> int:
    return (run_date - start_date).days + 1


def pick_day_config(day_number: int) -> dict | None:
    if day_number < 1 or day_number > 30:
        return None
    day_config = falowen30DayBlogCalendar.get(f"day_{day_number}")
    if day_config is None:
        return None
    return {**day_config, "content_type": CONTENT_TYPE_BY_DAY.get(day_number, "promo_essay")}


def normalize_unsplash_image_url(url: str) -> str:
    prefix = "https://unsplash.com/s/photos/"
    if not url.startswith(prefix):
        return url

    query = url.removeprefix(prefix).strip().replace("-", ",")
    return f"https://source.unsplash.com/featured/?{query}"


def _build_promo_essay(day_number: int, day_config: dict) -> str:
    variation = DAILY_MESSAGE_VARIATIONS[day_number - 1]
    paragraphs = [
        (
            f"{day_config['excerpt']} This topic, **{day_config['keyword']}**, is practical for learners who want "
            "study, work, travel, and communication opportunities."
        ),
        (
            f"In this lesson we focus on **{day_config['focus']}**. When students apply this consistently, they build "
            "confidence, communicate more clearly, and avoid the common beginner cycle of memorizing without using."
        ),
        (
            f"{BASE_FALOWEN_ANGLE} {day_config['promotion_angle']} Keep this daily reminder in mind: "
            f"{variation}"
        ),
        day_config["cta"],
    ]
    return "\n\n".join(paragraphs) + "\n"


def _build_grammar_notes(day_number: int, day_config: dict) -> str:
    return "\n".join(
        [
            f"**Intro:** {day_config['excerpt']}",
            "",
            (
                f"**Rule:** For this grammar topic on **{day_config['keyword']}**, keep your sentence pattern simple: "
                "use one clear structure first, then add detail with time or place expressions."
            ),
            "",
            "**Examples:**",
            "- *Ich lerne Deutsch.*",
            "- *Heute lerne ich Deutsch.*",
            "- *Lernst du heute?*",
            "",
            (
                "**Common mistake:** Mixing statement and question word order in one sentence, or placing the main "
                "verb too late."
            ),
            "",
            f"**Practice line:** Day {day_number}/30 — write 3 short sentences using this grammar rule and read them aloud.",
        ]
    ) + "\n"


def _build_vocabulary_notes(day_number: int, day_config: dict) -> str:
    return "\n".join(
        [
            f"**Intro:** {day_config['excerpt']}",
            "",
            "**Core words (topic set):**",
            "- **lernen** — to learn. *Ich lerne jeden Tag.*",
            "- **sprechen** — to speak. *Wir sprechen Deutsch im Kurs.*",
            "- **fragen** — to ask. *Ich frage den Lehrer.*",
            "",
            "**Useful connectors and context words:**",
            "- **heute** — today. *Heute üben wir Vokabeln.*",
            "- **morgen** — tomorrow. *Morgen wiederholen wir alles.*",
            "- **bitte** — please. *Bitte helfen Sie mir.*",
            "",
            (
                f"**Practical usage line:** Day {day_number}/30 — pick 5 words from today's **{day_config['keyword']}** "
                "topic and create your own mini dialogue."
            ),
        ]
    ) + "\n"


def _build_how_to_guide(day_number: int, day_config: dict) -> str:
    return "\n".join(
        [
            f"{day_config['excerpt']} Follow these steps and keep your output short and clear.",
            "",
            "**Step 1:** Learn and repeat 5 key words linked to this topic.",
            "",
            (
                "**Step 2:** Build 3 short sentences using one structure. Example: "
                "*Ich lerne heute Deutsch.* / *Ich komme aus Ghana.*"
            ),
            "",
            "**Step 3:** Say the sentences out loud twice, then write one extra personal sentence.",
            "",
            (
                f"**Step 4:** Turn your lines into a mini paragraph connected to **{day_config['focus']}** and "
                "share it for feedback."
            ),
            "",
            f"**CTA:** {day_config['cta']}",
        ]
    ) + "\n"


def _build_list_post(day_number: int, day_config: dict) -> str:
    return "\n".join(
        [
            f"{day_config['excerpt']} Here are practical points you can apply immediately.",
            "",
            "1. **Start small and consistent**  ",
            "   Study for 20–30 minutes daily instead of waiting for a perfect long session.",
            "",
            "2. **Use what you learn immediately**  ",
            "   Turn each new word or rule into one sentence about your own life.",
            "",
            "3. **Review actively**  ",
            "   Read aloud, write from memory, and compare with correct examples.",
            "",
            "4. **Track one improvement metric**  ",
            "   For example: number of sentences spoken per day or vocabulary retained weekly.",
            "",
            "5. **Ask for feedback quickly**  ",
            "   Short feedback loops prevent fossilized mistakes and speed up confidence.",
            "",
            f"Day {day_number}/30 CTA: {day_config['cta']}",
        ]
    ) + "\n"


def build_body(day_number: int, day_config: dict) -> str:
    content_type = day_config.get("content_type", "promo_essay")

    if content_type == "grammar_notes":
        return _build_grammar_notes(day_number, day_config)
    if content_type == "vocabulary_notes":
        return _build_vocabulary_notes(day_number, day_config)
    if content_type == "how_to_guide":
        return _build_how_to_guide(day_number, day_config)
    if content_type == "list_post":
        return _build_list_post(day_number, day_config)
    return _build_promo_essay(day_number, day_config)


def build_post(day_config: dict, body: str, publish_date: date) -> str:
    slug = day_config.get("slug") or slugify(day_config["title"])
    tags = ["falowen", "german", "30-day-blog", slug]
    tag_string = ", ".join(tags)

    image_url = normalize_unsplash_image_url(day_config["unsplash_link"])

    front_matter = [
        "---",
        "layout: post",
        f'title: "{day_config["title"]}"',
        f"date: {publish_date.isoformat()}",
        f"tags: [{tag_string}]",
        f"categories: [{day_config['category']}]",
        f'excerpt: "{day_config["excerpt"]}"',
        f"image: {image_url}",
        f'image_alt: "{day_config["title"]}"',
        f"permalink: /{slug}/",
        "seo:",
        f'  title: "{day_config["meta_title"]}"',
        f'  description: "{day_config["meta_description"]}"',
        "---",
        "",
    ]

    return "\n".join(front_matter) + body


def main() -> int:
    args = parse_args()
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    run_date = resolve_date(args.date)
    start_date = resolve_date(args.start_date, DEFAULT_START_DATE)
    day_number = compute_day_number(run_date, start_date)

    day_config = pick_day_config(day_number)
    if day_config is None:
        print(f"No post scheduled for {run_date.isoformat()} (day index: {day_number}).")
        return 0

    filename = f"{run_date.isoformat()}-{day_config['slug']}.md"
    post_path = POSTS_DIR / filename

    if args.dry_run:
        print(f"[dry-run] run_date={run_date.isoformat()} start_date={start_date.isoformat()} day={day_number}")
        print(f"[dry-run] title={day_config['title']}")
        print(f"[dry-run] file={post_path}")
        return 0

    if post_path.exists() and not args.force:
        print(f"Post already exists: {post_path}")
        return 0

    body = build_body(day_number, day_config)
    post_md = build_post(day_config, body, run_date)
    post_path.write_text(post_md, encoding="utf-8")
    print(f"Created day {day_number}: {post_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
