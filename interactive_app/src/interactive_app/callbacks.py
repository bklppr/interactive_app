#!/usr/bin/env python
 
from interactive_app import utils


def callback_button_reset(source, surface):
    """Callback for reset button."""
    source.data = {k: [] for k in list(source.data.keys())}
    surface.data = {k: [] for k in list(surface.data.keys())}


def callback_add_dot_on_double_tap(event, state, source):
    """Callback for adding dot on double tap."""
    coords = {'x': event.x, 'y': event.y, 'level': state.current_level[0],
              'color': state.color_dict[state.current_level[0]]}
    source.data = {k: v + [coords[k]] for k, v in source.data.items()}


def callback_button_update(source, classifiers, state, surface):
    """Callback for button to update the decision surface."""
    df = source.to_df()
    model = classifiers[state.current_model[0]]
    df = utils.create_decision_surface(model, df[['x', 'y']].values, df['level'].values, state.xlim, state.ylim,
                                       state.step)
    df.columns = ['x', 'y', 'level']
    df['color'] = [state.color_dict[i] for i in df['level'].values]
    surface.data = {c: s.tolist() for c, s in df.items()}


def callback_change_current_state(event, current_state):
    """Callback for updating current state.

    :param event: event to become the new current state.
    :param current_state: list of length 1 containing the current state to be replaced by event.
    """
    current_state.pop()
    current_state.append(event)
