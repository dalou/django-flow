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
        flow.set_active(focused);
    },
    is_focused: function(focused)
    {
        return this._focused;
    },
});



flow.on('flow_ready', function(delay, last_activity, activity_checker)
{

    flow.set_focused(true);
    $(window).focus(function()
    {
        flow.set_focused(true);
    }).blur(function()
    {
        flow.set_focused(false);
    });

    last_activity = new Date();
    activity_checker = function()
    {
        var now = new Date();
        if(now - last_activity >= flow._activity_delay)
        {

            flow.set_active(false);
            clearInterval(flow._activity_interval);
            to_activity = null;
        }
    }

    $(window).mousemove(function()
    {
        last_activity = new Date();
        if(!flow._activity_interval)
        {
            flow._activity_interval = setInterval(activity_checker, flow.__activity_delay); //every 10sec
            flow.set_active(true);
        }
    });
    flow._activity_interval = setInterval(activity_checker, flow.__activity_delay);
});