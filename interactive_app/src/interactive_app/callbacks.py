import utils

def callback_button_reset(wrapped_source, coordinates, wrapped_surface):
    """Callback for reset button."""
    wrapped_source.obj.data = {k: [] for k in list(wrapped_source.obj.data.keys())}
    coordinates.clear()
    wrapped_surface.obj.data = {k: [] for k in list(wrapped_surface.obj.data.keys())}

def callback_add_dot_on_double_tap(event, current_level, color_dict, coordinates,
                                   wrapped_source, colnames_color):
    """Callback for adding dot on double tap."""
    coords = (event.x, event.y, current_level[0], color_dict[current_level[0]])
    coordinates.append(coords)
    wrapped_source.obj.data = {k: [co[i] for co in coordinates] for i, k in enumerate(colnames_color)}

def callback_button_update(wrapped_source, classifiers, current_model, xlim, ylim, step,
                           color_dict, wrapped_surface):
    """Callback for button to update the decision surface."""
    df = wrapped_source.obj.to_df()
    model = classifiers[current_model[0]]
    df = utils.create_decision_surface(model, df[['x', 'y']].values, df['level'].values,
                                    xlim, ylim, step)
    df.columns = ['x', 'y', 'level']
    df['color'] = [color_dict[i] for i in df['level'].values]
    wrapped_surface.obj.data = {c: s.tolist() for c, s in df.items()}

def callback_button_class(event, current_level):
    """Callback for button to choose the class."""
    current_level.pop()
    current_level.append(event)

def callback_button_select_model(event, current_model):
    """Callback for button to choose the class."""
    current_model.pop()
    current_model.append(event)
