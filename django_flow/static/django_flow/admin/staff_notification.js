function NotificationNav(data, self)
{
    self = this;
    self.counter = 0;
    self.$notification = $('#nav_alerts');
    self.$notification.on('click', 'a', function()
    {
        for(var pk in flow._notifications)
        {
            var n = flow._notifications[pk];
            if(!n.is_read)
            {
                n.notify();
            }
        }
    });
};

NotificationNav.prototype.refresh_counter = function()
{
    this.counter = 0;
    console.log(flow._notifications)
    for(var pk in flow._notifications)
    {
        if(!flow._notifications[pk].is_read)
        {
            this.counter += 1;
        }
    }
    this.$notification.find('.alerts')[this.counter >= 1 ? 'addClass': 'removeClass']('active');
    this.$notification.find('#nav_alerts_counter').text(this.counter >= 1 ? this.counter : '');
};

var StaffNotification = function(data, self)
{
    self = this;
    // Unmutable atrributes
    // Same data that sent by to_json python model method
    for(var i in data) { self[i] = data[i]; }
    self.noty_instance = null;
    self.$notification = $('<div>'+self.title+'</div>')
    $('#staff_notifications').append(self.$notification)
};

StaffNotification.prototype.notify = function(play_sound, self)
{
    self = this;
    if(play_sound)
    {
        var snd = new Audio(window.STATIC_URL+'sound/notification.mp3');
        snd.play();
    }
    // If not active launch browser notificaition
    if(!flow.is_active())
    {
        var instance = new flow._builtin_notification(
            self.title,
            {
                body: self.body,
                icon: self.image_url || window.STATIC_URL+'img/logo_128x128.png'
            }
        );
        instance.onclick = function()
        {
            $(window).blur();
            $(window).focus();
            flow.set_active(true);
            self.notify(false);
        };
        instance.onerror = null;
        instance.onshow = null;
        instance.onclose = null;
    }
    // If active focused user, launch a noty
    else
    {
        // There is already a noty displayed
        if(self.noty_instance)
        {
            self.noty_instance.close();
        }

        self.noty_instance = noty(
        {
            text: '<h3>'+self.title+'</h3>' + self.body,
            layout: 'topRight',
            type: 'success notification_tooltip '+self.tags,
            animation:
            {
                open: 'animated flipInX',
                close: 'animated flipOutX',
                easing: 'swing',
                speed: 500
            },
            callback: {
                onShow: null,
                afterShow: null,
                onClose: null,
                afterClose: null,
                onCloseClick: function ()
                {
                    // mark as read through flow pipe if its a DB notification
                    if(self.pk )
                    {
                        flow.send('notification_read', { pk: self.pk });
                    }
                },
            },
        });

    }
};

Notification.prototype.set_read = function(read)
{
    if(read != this.is_read)
    {
        this.is_read = read;
        flow.notification_nav.refresh_counter();
    }

};

flow = $.extend(flow,
{
    _staff_notifications: {},
    _last_notification: null,
    get_staff_notification: function(pk, data)
    {
        var notification = flow._staff_notifications[pk];
        if(!notification && data)
        {
            flow._staff_notifications[pk] = notification = new StaffNotification(data);
        }
        return notification;
    },
});

// First

flow.on('flow_ready', function()
{
    // flow.notification_nav = new NotificationNav();
});

// Second, each initials

flow.on('staff_notification_initial', function(data)
{
    notification = flow.get_staff_notification(data.pk, data);
});

// Then

flow.on('flow_loaded', function()
{
    flow._builtin_notification.requestPermission(function (permission) {
        //console.log(permission);
    });
    // flow.notification_nav.refresh_counter();

});

// Finally

flow.on('staff_notification_created', function(data)
{
    notification = flow.get_staff_notification(data.pk, data);
    // flow.notification_nav.refresh_counter();
    notification.notify(true);
});

flow.on('notification_changed', function(data)
{
    notification = flow.get_notification(data.pk, data);
    if(notification)
    {
        notification.set_read(data.is_read);
        flow.notification_nav.refresh_counter();
        if(!data.is_read)
        {
            notification.notify();
        }
    }
});

flow.on('instant_notification_created', function(data)
{
    flow.notify(data);
});
