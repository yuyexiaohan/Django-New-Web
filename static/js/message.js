//错误消息提示框

// python中的类似类的给构造方法
function Message() {
    var self = this;
    self.isAppended = false;
    self.wrapperHeight = 48;
    self.wrapperWidth = 300;
    self.initStyle();
    self.initElement();
    self.listenCloseEvent();
}

Message.prototype.initStyle = function () {
    var self = this;
    self.errorStyle = {
        'wrapper':{
            'background': '#f2dede',
            'color': '#993d3d'
        },
        'close':{
            'color': '#993d3d'
        }
    };
    self.successStyle = {
        'wrapper':{
            'background': '#dff0d8',
            'color': '#468847'
        },
        'close': {
            'color': "#468847"
        }
    };
    self.infoStyle = {
        'wrapper': {
            'background': '#d9edf7',
            'color': '#5bc0de'
        },
        'close': {
            'color': '#5bc0de'
        }
    }
};

Message.prototype.initElement = function () {
    var self = this;
    self.wrapper = $("<div></div>");
    self.wrapper.css({
        'padding': '10px',
        'font-size': '14px',
        'width': '300px',
        'position': 'fixed',
        'z-index': '2000',
        'left': '50%',
        'top': '-48px',
        'margin-left':'-150px',
        'height': '48px',
        'box-sizing': 'border-box',
        'border': '1px solid #ddd',
        'border-radius': '4px',
        'line-height': '24px',
        'font-weight': 700
    });
    self.closeBtn = $("<span>×</span>");
    self.closeBtn.css({
        'font-family': 'core_sans_n45_regular,"Avenir Next","Helvetica Neue",Helvetica,Arial,"PingFang SC","Source Han Sans SC","Hiragino Sans GB","Microsoft YaHei","WenQuanYi MicroHei",sans-serif;',
        'font-weight': '700',
        'float': 'right',
        'cursor': 'pointer',
        'font-size': '22px'
    });

    self.messageSpan = $("<span class='xfz-message-group'></span>");

    self.wrapper.append(self.messageSpan);
    self.wrapper.append(self.closeBtn);
};

Message.prototype.listenCloseEvent = function () {
    var self = this;
    self.closeBtn.click(function () {
        self.wrapper.animate({"top":-self.wrapperHeight});
    });
};

Message.prototype.showError = function (message) {
    this.show(message,'error');
};

Message.prototype.showSuccess = function (message) {
    this.show(message,'success');
};

Message.prototype.showInfo = function (message) {
    this.show(message,'info');
};

Message.prototype.show = function (message,type) {
    var self = this;
    if(!self.isAppended){
        $(document.body).append(self.wrapper);
        self.isAppended = true;
    }
    self.messageSpan.text(message);
    if(type === 'error') {
        self.wrapper.css(self.errorStyle['wrapper']);
        self.closeBtn.css(self.errorStyle['close']);
    }else if(type === 'info'){
        self.wrapper.css(self.infoStyle['wrapper']);
        self.closeBtn.css(self.infoStyle['close']);
    }else{
        self.wrapper.css(self.successStyle['wrapper']);
        self.closeBtn.css(self.successStyle['close']);
    }
    self.wrapper.animate({"top":0},function () {
        setTimeout(function () {
            self.wrapper.animate({"top":-self.wrapperHeight});
        },3000);
    });
};

window.messageBox = new Message();