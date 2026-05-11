import math
import pygame


TRUE_COLOR = (38, 220, 120)
FALSE_COLOR = (255, 90, 105)
AXIS_COLOR = (145, 156, 185)
GRID_COLOR = (58, 70, 105)
TEXT_COLOR = (232, 236, 255)
MUTED_TEXT = (155, 164, 190)
BG_COLOR = (28, 37, 60)
BORDER_COLOR = (82, 96, 132)
CYAN = (87, 221, 255)


def draw_truth_graph(surface, rect, truth_points, text_font, small_font):
    pygame.draw.rect(surface, BG_COLOR, rect, border_radius=16)
    pygame.draw.rect(surface, BORDER_COLOR, rect, 2, border_radius=16)

    if not truth_points:
        empty_surface = text_font.render(
            "Нет данных для построения графика истинности.",
            True,
            MUTED_TEXT,
        )
        empty_rect = empty_surface.get_rect(center=rect.center)
        surface.blit(empty_surface, empty_rect)
        return

    left_padding = 90
    right_padding = 35
    top_padding = 40
    bottom_padding = 75

    plot_rect = pygame.Rect(
        rect.left + left_padding,
        rect.top + top_padding,
        rect.width - left_padding - right_padding,
        rect.height - top_padding - bottom_padding,
    )

    if plot_rect.width <= 0 or plot_rect.height <= 0:
        return

    max_x = max(point[0] for point in truth_points)
    graph_min_x = 0
    graph_max_x = max(1, max_x)

    y_true = int(plot_rect.top + plot_rect.height * 0.25)
    y_false = int(plot_rect.top + plot_rect.height * 0.75)

    pygame.draw.line(surface, GRID_COLOR, (plot_rect.left, y_true), (plot_rect.right, y_true), 1)
    pygame.draw.line(surface, GRID_COLOR, (plot_rect.left, y_false), (plot_rect.right, y_false), 1)

    pygame.draw.line(surface, AXIS_COLOR, (plot_rect.left, plot_rect.top), (plot_rect.left, plot_rect.bottom), 2)
    pygame.draw.line(surface, AXIS_COLOR, (plot_rect.left, plot_rect.bottom), (plot_rect.right, plot_rect.bottom), 2)

    true_label = text_font.render("true", True, TRUE_COLOR)
    false_label = text_font.render("false", True, FALSE_COLOR)

    surface.blit(true_label, true_label.get_rect(midright=(plot_rect.left - 12, y_true)))
    surface.blit(false_label, false_label.get_rect(midright=(plot_rect.left - 12, y_false)))

    tick_count = 6
    tick_values = []

    for i in range(tick_count):
        value = round(graph_min_x + (graph_max_x - graph_min_x) * i / (tick_count - 1))

        if value not in tick_values:
            tick_values.append(value)

    if 0 not in tick_values:
        tick_values.insert(0, 0)

    for value in tick_values:
        px = plot_rect.left + (value - graph_min_x) / (graph_max_x - graph_min_x) * plot_rect.width
        px = int(px)

        pygame.draw.line(surface, AXIS_COLOR, (px, plot_rect.bottom), (px, plot_rect.bottom + 6), 1)

        value_surface = small_font.render(str(value), True, TEXT_COLOR)
        value_rect = value_surface.get_rect(midtop=(px, plot_rect.bottom + 10))
        surface.blit(value_surface, value_rect)

    x_label = small_font.render("n", True, TEXT_COLOR)
    surface.blit(x_label, x_label.get_rect(midtop=(plot_rect.centerx, plot_rect.bottom + 34)))

    point_radius = 4

    if len(truth_points) > 1000:
        point_radius = 3

    if len(truth_points) > 5000:
        point_radius = 2

    for x_value, is_true in truth_points:
        px = plot_rect.left + (x_value - graph_min_x) / (graph_max_x - graph_min_x) * plot_rect.width
        py = y_true if is_true else y_false
        color = TRUE_COLOR if is_true else FALSE_COLOR

        pygame.draw.circle(surface, color, (int(px), int(py)), point_radius)

    pygame.draw.circle(surface, TRUE_COLOR, (rect.right - 190, rect.top + 24), 6)
    legend_true = small_font.render("гипотеза верна", True, TEXT_COLOR)
    surface.blit(legend_true, (rect.right - 176, rect.top + 14))

    pygame.draw.circle(surface, FALSE_COLOR, (rect.right - 190, rect.top + 50), 6)
    legend_false = small_font.render("гипотеза неверна", True, TEXT_COLOR)
    surface.blit(legend_false, (rect.right - 176, rect.top + 40))


import math
import pygame

BG_COLOR = (28, 38, 62)
BORDER_COLOR = (90, 105, 145)
GRID_COLOR = (60, 74, 108)
AXIS_COLOR = (180, 190, 220)
TEXT_COLOR = (230, 235, 255)
MUTED_TEXT = (150, 160, 190)
LINE_COLOR = (255, 208, 90)
POINT_COLOR = (255, 208, 90)
CYAN = (88, 221, 255)


def nice_step(value):
    if value <= 0:
        return 1

    power = math.floor(math.log10(value))
    base = 10 ** power
    fraction = value / base

    if fraction <= 1:
        return base
    if fraction <= 2:
        return 2 * base
    if fraction <= 5:
        return 5 * base
    return 10 * base


import math
import pygame


BG_COLOR = (28, 38, 62)
BORDER_COLOR = (90, 105, 145)
GRID_COLOR = (60, 74, 108)
AXIS_COLOR = (200, 210, 235)
TEXT_COLOR = (230, 235, 255)
MUTED_TEXT = (150, 160, 190)
POINT_COLOR = (110, 220, 255)


def nice_step(value):
    if value <= 0:
        return 1

    power = math.floor(math.log10(value))
    base = 10 ** power
    fraction = value / base

    if fraction <= 1:
        return base
    if fraction <= 2:
        return 2 * base
    if fraction <= 5:
        return 5 * base
    return 10 * base


def draw_function_graph(
    surface,
    rect,
    points,
    text_font,
    small_font,
    zoom,
    mouse_pos,
    pan_x=0,
    pan_y=0,
):
    pygame.draw.rect(surface, BG_COLOR, rect, border_radius=16)
    pygame.draw.rect(surface, BORDER_COLOR, rect, 2, border_radius=16)

    if len(points) < 2:
        empty_surface = text_font.render(
            "Введите функцию и нажмите «Построить».",
            True,
            MUTED_TEXT,
        )
        empty_rect = empty_surface.get_rect(center=rect.center)
        surface.blit(empty_surface, empty_rect)
        return None

    numeric_points = []

    for x, y in points:
        if isinstance(y, (int, float)) and math.isfinite(float(y)):
            numeric_points.append((x, float(y)))

    if len(numeric_points) < 2:
        empty_surface = text_font.render(
            "Недостаточно числовых точек для построения.",
            True,
            MUTED_TEXT,
        )
        empty_rect = empty_surface.get_rect(center=rect.center)
        surface.blit(empty_surface, empty_rect)
        return None

    xs = [point[0] for point in numeric_points]
    ys = [point[1] for point in numeric_points]

    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    if min_x == max_x:
        min_x -= 1
        max_x += 1

    if min_y == max_y:
        min_y -= 1
        max_y += 1

    padding_left = 60
    padding_right = 20
    padding_top = 20
    padding_bottom = 50

    plot_rect = pygame.Rect(
        rect.left + padding_left,
        rect.top + padding_top,
        rect.width - padding_left - padding_right,
        rect.height - padding_top - padding_bottom,
    )

    data_width = max_x - min_x
    data_height = max_y - min_y

    scale_x = plot_rect.width / data_width
    scale_y = plot_rect.height / data_height

    unit_scale = min(scale_x, scale_y) * zoom
    unit_scale = max(0.001, unit_scale)

    center_x_value = (min_x + max_x) / 2
    center_y_value = (min_y + max_y) / 2

    def to_screen(x, y):
        px = plot_rect.centerx + (x - center_x_value) * unit_scale + pan_x
        py = plot_rect.centery - (y - center_y_value) * unit_scale + pan_y
        return int(px), int(py)

    visible_min_x = center_x_value - (plot_rect.width / 2 + pan_x) / unit_scale
    visible_max_x = center_x_value + (plot_rect.width / 2 - pan_x) / unit_scale
    visible_min_y = center_y_value - (plot_rect.height / 2 - pan_y) / unit_scale
    visible_max_y = center_y_value + (plot_rect.height / 2 + pan_y) / unit_scale

    pygame.draw.rect(surface, (24, 33, 56), plot_rect)

    tick_step_x = nice_step(max((visible_max_x - visible_min_x) / 7, 1))
    tick_step_y = nice_step(max((visible_max_y - visible_min_y) / 6, 1))

    current_x = math.floor(visible_min_x / tick_step_x) * tick_step_x
    while current_x <= visible_max_x:
        px, _ = to_screen(current_x, center_y_value)

        if plot_rect.left <= px <= plot_rect.right:
            pygame.draw.line(
                surface,
                GRID_COLOR,
                (px, plot_rect.top),
                (px, plot_rect.bottom),
                1,
            )

            label = small_font.render(str(round(current_x, 2)), True, MUTED_TEXT)
            label_rect = label.get_rect(midtop=(px, plot_rect.bottom + 6))
            surface.blit(label, label_rect)

        current_x += tick_step_x

    current_y = math.floor(visible_min_y / tick_step_y) * tick_step_y
    while current_y <= visible_max_y:
        _, py = to_screen(center_x_value, current_y)

        if plot_rect.top <= py <= plot_rect.bottom:
            pygame.draw.line(
                surface,
                GRID_COLOR,
                (plot_rect.left, py),
                (plot_rect.right, py),
                1,
            )

            label = small_font.render(str(round(current_y, 2)), True, MUTED_TEXT)
            label_rect = label.get_rect(midright=(plot_rect.left - 8, py))
            surface.blit(label, label_rect)

        current_y += tick_step_y

    if visible_min_y <= 0 <= visible_max_y:
        _, axis_y = to_screen(center_x_value, 0)
    else:
        axis_y = plot_rect.bottom

    if visible_min_x <= 0 <= visible_max_x:
        axis_x, _ = to_screen(0, center_y_value)
    else:
        axis_x = plot_rect.left

    pygame.draw.line(
        surface,
        AXIS_COLOR,
        (plot_rect.left, axis_y),
        (plot_rect.right, axis_y),
        2,
    )

    pygame.draw.line(
        surface,
        AXIS_COLOR,
        (axis_x, plot_rect.top),
        (axis_x, plot_rect.bottom),
        2,
    )

    x_label = small_font.render("X", True, TEXT_COLOR)
    y_label = small_font.render("Y", True, TEXT_COLOR)

    surface.blit(
        x_label,
        (plot_rect.right - 18, axis_y + 6 if axis_y < plot_rect.bottom - 20 else plot_rect.bottom + 4),
    )
    surface.blit(y_label, (axis_x + 6, plot_rect.top + 2))

    hovered = None
    visible_points = []

    for x, y in numeric_points:
        px, py = to_screen(x, y)

        if plot_rect.left <= px <= plot_rect.right and plot_rect.top <= py <= plot_rect.bottom:
            visible_points.append((x, y, px, py))

    for x, y, px, py in visible_points:
        pygame.draw.circle(surface, POINT_COLOR, (px, py), 4)

        if math.hypot(mouse_pos[0] - px, mouse_pos[1] - py) <= 8:
            hovered = (x, y, px, py)

    if hovered is not None:
        x, y, px, py = hovered

        tooltip_text = f"x = {x}, y = {round(y, 5)}"
        tooltip_surface = small_font.render(tooltip_text, True, TEXT_COLOR)
        tooltip_rect = tooltip_surface.get_rect()
        tooltip_rect.topleft = (px + 12, py - 32)
        tooltip_rect.inflate_ip(18, 12)

        pygame.draw.rect(surface, (18, 25, 44), tooltip_rect, border_radius=8)
        pygame.draw.rect(surface, BORDER_COLOR, tooltip_rect, 1, border_radius=8)
        surface.blit(tooltip_surface, (tooltip_rect.left + 9, tooltip_rect.top + 6))

    info = small_font.render(
        f"Масштаб: {round(zoom, 2)}x | Колёсико: масштаб | ЛКМ по графику: двигать",
        True,
        MUTED_TEXT,
    )
    surface.blit(info, (rect.left + 18, rect.bottom - 30))

    return hovered