flow = $.extend(flow,
{
    ACTIVITY_DELAY: window.FLOW_ACTIVITY_DELAY, // in MS
    _activity_interval: null,
    _active: false,
    set_active: function(active)
    {
        if(active != this._active)
        {
            this._active = active;
            this._dispatch('activity_changed', active);
        }
    },
    is_active: function(active)
    {
        return this._active;
    },
    _focused: false,
    set_focused: function(focused)
    {
        if(focused != this._focused)
        {
            this._focused = focused;
            this._dispatch('focus_changed', focused);
        }
    },
    is_focused: function(focused)
    {
        return this._focused;
    },
});

flow.on('activity_changed', function()
{
    if(flow.is_active())
    {
        flow._disconnected_receive();
    }
});

flow.on('flow_ready', function(delay, activity_checker)
{
    flow.set_focused(true);
    $(window).focus(function()
    {
        flow.set_focused(true);
        flow._disconnected_receive(100);
    }).blur(function()
    {
        flow.set_focused(false);
    });

    flow._last_activity = new Date();
    activity_checker = function()
    {
        var now = new Date();
        flow._last_activity_interval = now - flow._last_activity
        if(flow._last_activity_interval >= flow._activity_delay)
        {

            flow.set_active(false);
            clearInterval(flow._activity_interval);
            to_activity = null;
        }
    }

    $(window).mousemove(function()
    {
        flow._last_activity = new Date();
        if(!flow._activity_interval)
        {
            flow._activity_interval = setInterval(activity_checker, flow.__activity_delay); //every 10sec
            flow.set_active(true);
        }
    });
    flow._activity_interval = setInterval(activity_checker, flow.__activity_delay);
});