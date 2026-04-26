import pygame


TRUE_COLOR = (40, 170, 70)
FALSE_COLOR = (210, 70, 70)
AXIS_COLOR = (70, 70, 90)
GRID_COLOR = (210, 210, 225)
TEXT_COLOR = (40, 40, 60)
BG_COLOR = (255, 255, 255)
BORDER_COLOR = (160, 160, 180)


def draw_truth_graph(surface, rect, truth_points, text_font, small_font):
    pygame.draw.rect(surface, BG_COLOR, rect, border_radius=12)
    pygame.draw.rect(surface, BORDER_COLOR, rect, 2, border_radius=12)

    if not truth_points:
        empty_surface = text_font.render(
            "Нет данных для построения графика истинности.",
            True,
            (100, 100, 120),
        )
        empty_rect = empty_surface.get_rect(center=rect.center)
        surface.blit(empty_surface, empty_rect)
        return

    left_padding = 90
    right_padding = 35
    top_padding = 35
    bottom_padding = 70

    plot_rect = pygame.Rect(
        rect.left + left_padding,
        rect.top + top_padding,
        rect.width - left_padding - right_padding,
        rect.height - top_padding - bottom_padding,
    )

    if plot_rect.width <= 0 or plot_rect.height <= 0:
        return

    min_x = min(point[0] for point in truth_points)
    max_x = max(point[0] for point in truth_points)

    graph_min_x = 0
    graph_max_x = max_x

    if graph_max_x == graph_min_x:
        graph_max_x = graph_min_x + 1

    y_true = int(plot_rect.top + plot_rect.height * 0.25)
    y_false = int(plot_rect.top + plot_rect.height * 0.75)

    pygame.draw.line(
        surface,
        GRID_COLOR,
        (plot_rect.left, y_true),
        (plot_rect.right, y_true),
        1,
    )
    pygame.draw.line(
        surface,
        GRID_COLOR,
        (plot_rect.left, y_false),
        (plot_rect.right, y_false),
        1,
    )

    pygame.draw.line(
        surface,
        AXIS_COLOR,
        (plot_rect.left, plot_rect.top),
        (plot_rect.left, plot_rect.bottom),
        2,
    )
    pygame.draw.line(
        surface,
        AXIS_COLOR,
        (plot_rect.left, plot_rect.bottom),
        (plot_rect.right, plot_rect.bottom),
        2,
    )

    true_label = text_font.render("true", True, TRUE_COLOR)
    false_label = text_font.render("false", True, FALSE_COLOR)

    true_label_rect = true_label.get_rect(
        midright=(plot_rect.left - 12, y_true)
    )
    false_label_rect = false_label.get_rect(
        midright=(plot_rect.left - 12, y_false)
    )

    surface.blit(true_label, true_label_rect)
    surface.blit(false_label, false_label_rect)

    x_label = small_font.render("n", True, TEXT_COLOR)
    x_label_rect = x_label.get_rect(
        midtop=(plot_rect.centerx, plot_rect.bottom + 34)
    )
    surface.blit(x_label, x_label_rect)

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

        pygame.draw.line(
            surface,
            AXIS_COLOR,
            (px, plot_rect.bottom),
            (px, plot_rect.bottom + 6),
            1,
        )

        value_surface = small_font.render(str(value), True, TEXT_COLOR)
        value_rect = value_surface.get_rect(midtop=(px, plot_rect.bottom + 10))
        surface.blit(value_surface, value_rect)

    point_radius = 4

    if len(truth_points) > 1000:
        point_radius = 3

    if len(truth_points) > 5000:
        point_radius = 2

    for x_value, is_true in truth_points:
        px = plot_rect.left + (x_value - graph_min_x) / (graph_max_x - graph_min_x) * plot_rect.width

        py = y_true if is_true else y_false
        color = TRUE_COLOR if is_true else FALSE_COLOR

        pygame.draw.circle(
            surface,
            color,
            (int(px), int(py)),
            point_radius,
        )

    legend_true_rect = pygame.Rect(rect.right - 200, rect.top + 16, 14, 14)
    pygame.draw.circle(surface, TRUE_COLOR, legend_true_rect.center, 6)
    legend_true_text = small_font.render("гипотеза верна", True, TEXT_COLOR)
    surface.blit(legend_true_text, (legend_true_rect.right + 8, rect.top + 9))

    legend_false_rect = pygame.Rect(rect.right - 200, rect.top + 40, 14, 14)
    pygame.draw.circle(surface, FALSE_COLOR, legend_false_rect.center, 6)
    legend_false_text = small_font.render("гипотеза неверна", True, TEXT_COLOR)
    surface.blit(legend_false_text, (legend_false_rect.right + 8, rect.top + 33))