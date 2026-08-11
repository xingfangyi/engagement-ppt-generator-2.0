from collections import Counter


BELONGING_ACTIONS = [
    "Organize annual family events such as an annual dinner including family members.",
    "Arrange regular site visits by Sales and PMs to listen to employees' needs and feedback.",
    "Continue to provide safety and resilience training.",
    "Arrange alternative team activities for employees unable to join the main outing.",
    "Provide proper and timely recognition for extra contributions.",
    "Share best practices and success stories across the team.",
]

WORK_LIFE_BALANCE_ACTIONS = [
    "Assess available maintenance time windows in the sales phase to avoid excessive overtime.",
    "Project managers proactively communicate with customers to reduce unnecessary overtime.",
    "Arrange regular care check-ins for field and site employees.",
    "Assign service sites closer to employees where feasible.",
    "Review annual leave quarterly and ensure leave is fully utilized.",
    "Promote inclusive recognition activities to improve team energy and morale.",
]


def detect_focus_areas(bottom_10):
    keyword_map = {
        "belonging": [
            "inclusion", "recognition", "fair treatment", "manager trust",
            "feedback", "values", "company direction", "action taking"
        ],
        "work_life_balance": [
            "well-being", "barriers to execution", "empowerment",
            "rewards", "challenge status quo", "development"
        ],
    }

    counter = Counter()

    for item in bottom_10:
        text = f"{item['driver']} {item['statement']}".lower()
        for topic, keywords in keyword_map.items():
            for kw in keywords:
                if kw in text:
                    counter[topic] += 1

    if not counter:
        counter["belonging"] = 1
        counter["work_life_balance"] = 1

    top_two = [x[0] for x in counter.most_common(2)]

    if "belonging" not in top_two:
        top_two.append("belonging")
    if "work_life_balance" not in top_two:
        top_two.append("work_life_balance")

    return top_two[:2]


def generate_actions(data):
    focus_areas = detect_focus_areas(data["bottom_10"])

    actions = {
        "left_topic": "Belonging",
        "right_topic": "Work Life Balance",
        "left_question": "I feel a sense of belong at ABB.",
        "right_question": "I am able to successfully balance my work and personal life.",
        "left_actions": BELONGING_ACTIONS,
        "right_actions": WORK_LIFE_BALANCE_ACTIONS,
        "focus_areas": focus_areas,
    }

    return actions
