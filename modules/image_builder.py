import os
from PIL import Image, ImageDraw, ImageFont

ABB_RED = (255, 0, 15)
ABB_LILAC = (103, 100, 246)
BLACK = (30, 30, 30)
GRAY = (110, 110, 110)
WHITE = (255, 255, 255)


def _get_font(size=24, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Arial.ttf",
        "arial.ttf",
    ]
    for p in candidates:
        try:
            return ImageFont.truetype(p, size=size)
        except Exception:
            continue
    return ImageFont.load_default()


def _wrap(draw, text, font, max_width):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test = current + (" " if current else "") + word
        if draw.textlength(test, font=font) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _draw_wrapped_text(draw, text, xy, font, fill, max_width, line_gap=6):
    x, y = xy
    lines = _wrap(draw, text, font, max_width)
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + line_gap
    return y


def build_overview_images(data, out_dir):
    left_path = os.path.join(out_dir, "overview_left.png")
    right_path = os.path.join(out_dir, "overview_right.png")

    # Left image
    img = Image.new("RGB", (1400, 650), WHITE)
    draw = ImageDraw.Draw(img)
    font_title = _get_font(34, True)
    font_big = _get_font(78, True)
    font_sub = _get_font(24, False)
    font_small = _get_font(22, False)

    draw.rounded_rectangle((30, 30, 1370, 620), radius=24, outline=ABB_LILAC, width=4)
    draw.text((60, 50), "Survey Overview", font=font_title, fill=ABB_LILAC)

    cards = [
        (70, 150, 420, 520, "Engagement", str(data["overall_score"]), ABB_RED),
        (490, 150, 840, 520, "Company", str(data["company_score"]), ABB_LILAC),
        (910, 150, 1260, 520, "Responded", str(data["responded_count"]), ABB_RED),
    ]

    for x1, y1, x2, y2, label, value, color in cards:
        draw.rounded_rectangle((x1, y1, x2, y2), radius=20, fill=(250, 250, 250), outline=color, width=4)
        draw.text((x1 + 30, y1 + 30), label, font=font_sub, fill=GRAY)
        draw.text((x1 + 30, y1 + 130), value, font=font_big, fill=color)

    draw.text((70, 560), f"Department: {data['department']}", font=font_small, fill=BLACK)
    img.save(left_path)

    # Right image
    img = Image.new("RGB", (1100, 650), WHITE)
    draw = ImageDraw.Draw(img)
    font_title = _get_font(32, True)
    font_body = _get_font(24, False)
    font_label = _get_font(22, True)

    draw.rounded_rectangle((25, 25, 1075, 625), radius=24, outline=ABB_RED, width=4)
    draw.text((50, 45), "Key Facts", font=font_title, fill=ABB_RED)

    y = 120
    facts = [
        f"Survey month: {data['survey_month']}",
        f"Questions: {data['question_count']}",
        f"Vs company: {data['company_score']}",
        f"Change vs last survey: {data['change_vs_last']}",
    ]
    for fact in facts:
        draw.text((60, y), f"• {fact}", font=font_body, fill=BLACK)
        y += 52

    draw.text((60, y + 20), "Lowest-scoring topics", font=font_label, fill=ABB_LILAC)
    y += 80

    for item in data["bottom_10"][:3]:
        text = f"{item['driver']} ({item['score']})"
        draw.text((60, y), f"• {text}", font=font_body, fill=BLACK)
        y += 46

    img.save(right_path)
    return left_path, right_path


def build_strengths_image(items, title, out_path, color):
    img = Image.new("RGB", (1200, 650), WHITE)
    draw = ImageDraw.Draw(img)
    font_title = _get_font(32, True)
    font_head = _get_font(24, True)
    font_body = _get_font(22, False)
    font_impact = _get_font(20, True)

    draw.rounded_rectangle((25, 25, 1175, 625), radius=24, outline=color, width=4)
    draw.text((45, 45), title, font=font_title, fill=color)

    y = 120
    for idx, item in enumerate(items, start=1):
        draw.rounded_rectangle((45, y, 1135, y + 150), radius=18, fill=(248, 248, 248), outline=(220, 220, 220), width=2)
        draw.text((65, y + 18), f"{idx}. {item['title']}", font=font_head, fill=BLACK)
        _draw_wrapped_text(draw, item["statement"], (65, y + 58), font_body, GRAY, 940, line_gap=4)
        draw.text((920, y + 108), item["impact"], font=font_impact, fill=color)
        y += 170

    img.save(out_path)
    return out_path


def build_bottom10_panel(rows, title, out_path):
    img = Image.new("RGB", (1200, 900), WHITE)
    draw = ImageDraw.Draw(img)
    font_title = _get_font(28, True)
    font_head = _get_font(18, True)
    font_body = _get_font(16, False)
    font_score = _get_font(30, True)

    draw.rounded_rectangle((25, 25, 1175, 875), radius=24, outline=ABB_RED, width=4)
    draw.text((45, 45), title, font=font_title, fill=ABB_RED)

    y = 110
    for item in rows:
        draw.rounded_rectangle((45, y, 1135, y + 140), radius=16, fill=(249, 249, 249), outline=(225, 225, 225), width=2)

        draw.text((65, y + 18), str(item["score"]), font=font_score, fill=ABB_RED)
        draw.text((150, y + 18), item["driver"], font=font_head, fill=BLACK)

        statement = item["statement"]
        _draw_wrapped_text(draw, statement, (150, y + 48), font_body, GRAY, 780, line_gap=3)

        meta = f"vs Company: {item['vs_company']}   |   Change: {item['change']}   |   Impact: {item['impact']}"
        draw.text((150, y + 104), meta, font=font_body, fill=BLACK)

        y += 155

    img.save(out_path)
    return out_path
