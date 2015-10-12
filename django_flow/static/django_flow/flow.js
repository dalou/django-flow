
var Notification = window.Notification || window.mozNotification || window.webkitNotification;

Notification.requestPermission(function (permission) {
    // console.log(permission);
});



var flow =
{
    _ready: false,
    _loaded: false,
    _connected: false,
    _focus: false,
    _listeners: {},
    DEBUG: window.FLOW_DEBUG,
    INITIAL_URL: window.FLOW_INITIAL_URL,
    DISCONNECTED_ENABLED: window.FLOW_DISCONNECTED_ENABLED,
    DISCONNECTED_RECEIVE_URL: window.FLOW_DISCONNECTED_RECEIVE_URL,
    DISCONNECTED_SEND_URL: window.FLOW_DISCONNECTED_SEND_URL,
    WS_ENABLED: window.FLOW_WS_ENABLED,
    WS_URI: window.FLOW_WS_URI,
    WS_HEARTBEAT: window.FLOW_WS_HEARTBEAT,
    _redis_ws: null,
    _builtin_notification: window.Notification || window.mozNotification || window.webkitNotification,

    _init: function(self)
    {
        self = this;
        if(!self._ready)
        {
            self._ready = true;
            self._dispatch('flow_ready');

            if(self.INITIAL_URL)
            {
                $.get(self.INITIAL_URL, null, function(wsdata)
                {
                    //console.log(wsdata)
                    for( var i in wsdata)
                    {
                        var data = wsdata[i];
                        if(self.DEBUG)
                        {
                            console.log('%c INITIAL ', data.type, 'background: #B1D3D4; color: #222', data.data);
                        }
                        self._dispatch(data.type, data.data);
                    }
                    self._loaded = true;
                    self._dispatch('flow_loaded');
                    self._connect();
                });
            }
            else
            {
                self._loaded = true;
                self._dispatch('flow_loaded');
                self._dispatch('flow_no_inital');
                self._connect();
                if(self.DEBUG)
                {
                    console.log('%c FLOW has no INITIAL_URL', 'color: #550000');
                }
                return;
            }


        }
    },
    _connect: function(self)
    {
        self = this;
        if(self.WS_ENABLED && self.WS_URI)
        {
            self = this;
            self._redis_ws = RedisWebSocket(
            {
                uri: self.WS_URI+'flow?subscribe-user&publish-user&echo',
                receive_message: self._receive,
                heartbeat_msg: self.WS_HEARTBEAT,
                on_open: function()
                {
                    setTimeout(function()
                    {
                        self._connected = true;
                        self._dispatch('flow_connected');
                    }, 500);
                },
                flow: self,
            });
        }
        else
        {
            self._dispatch('flow_ws_disabled');
            if(self.DEBUG)
            {
                console.log('%c FLOW websocket is disabled ', 'color: #550000');
            }
            if(self.DISCONNECTED_ENABLED)
            {
                self._disconnected_receive(2000);
            }
            else
            {
                if(self.DEBUG)
                {
                    console.log('%c FLOW disconnected is disabled ', 'color: #550000');
                }
            }
        }
    },
    on: function(type, fct)
    {
        var types = type.split(',')
        for(var i in types)
        {
            var type = $.trim(types[i]);
            listeners = this._listeners[type];
            if(!listeners) {
                this._listeners[type] = listeners = [];
            }
            listeners.push(fct);
        }
    },
    _disconnected_send: function(msg)
    {
        self = this;
        if(self.DISCONNECTED_ENABLED && self.DISCONNECTED_SEND_URL)
        {
            $.get(self.DISCONNECTED_SEND_URL, {msg:msg}, function(wsdata)
            {
                for(var i in wsdata)
                {
                    self._receive(wsdata[i]);
                }
            });
        }
    },
    send: function(type, data)
    {
        var typed_data = {}
        typed_data.type = type;
        typed_data.from = "js"
        typed_data.data = data
        var msg = JSON.stringify(typed_data);
        if(this._connected && this._redis_ws)
        {
            if(this.DEBUG)
            {
                console.log('%c SEND ', 'background: #222; color: #bada55', typed_data);
            }
            this._redis_ws.send_message(msg);
        }
        else
        {
            self._disconnected_send(msg);
        }
    },
    _disconnected_receive_timeout: null,
    _disconnected_receive: function(timeout)
    {
        self = this;
        console.log(timeout);
        if(self.DISCONNECTED_ENABLED && self.DISCONNECTED_RECEIVE_URL)
        {
            if(self._disconnected_receive_timeout)
            {
                clearTimeout(self._disconnected_receive_timeout);
            }
            self._disconnected_receive_timeout = setTimeout(function()
            {
                if(flow.is_active())
                {
                    $.get(self.DISCONNECTED_RECEIVE_URL, null, function(wsdata)
                    {
                        for(var i in wsdata)
                        {
                            self._receive(wsdata[i]);
                        }
                    });
                    self._disconnected_receive(flow.is_focused() ? 5000 : 20000);
                }
            }, timeout);
        }
    },
    _receive: function(msg)
    {
        var data = JSON.parse(msg);
        if(data && data.from != "js")
        {
            if(self.DEBUG)
            {
                console.log('%c RECEIVE ', 'background: #bada55; color: #222', data);
            }
            flow._dispatch(data.type, data.data);
        }
    },

    _dispatch: function(type, data)
    {
        if(this._listeners[type])
        {
            for(var i in this._listeners[type])
            {
                this._listeners[type][i](data)
                //console.log('LISTEN', json.type, json)
            }
        }
        else
        {
            // console.error('LISTEN', type+" has no listeners.", data)
        }
    }
}
$(document).ready(function(flow)
{
    window.flow._init();
});

window.flow = flow;











