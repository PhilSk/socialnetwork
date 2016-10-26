var config = {
    container: document.getElementById("content")
};

class Feed extends React.Component {

    state = {
        friendList: {},
        objects: {}
    };

    componentDidMount() {
        let _this = this;
        _this.setState({friendList: this.props.friendList});
        for(var i = 0; i < this.state.friendList.length; i++) {
            fetch('/api/posts/?user_id=' + this.state.friendList[i], {credentials: 'include'}).then(function (response) {
                console.log(response);
                response.json().then(function (data) {
                    console.log(data);
                    _this.setState({objects: this.state.objects + data});
                })
            }).catch(function (err) {
                console.log("Error", err);
            })
        }
    }

    render() {
        return (
            <div>
                <h3>Посты в твоей ленте</h3>
                <h3>Вот твои друзья бро!</h3>
            </div>
        );
    }
}

class Personal extends React.Component {

    state = {
        currentUserId: this.props.currentUserId,
        objects: []
    };

    componentDidMount() {
        let _this = this;

        fetch('/api/users/' + this.state.currentUserId + '/', {credentials: 'include'}).then(function (response) {
            console.log(response);
            response.json().then(function (data) {
                console.log(data);
                _this.setState({objects: data});
            })
        }).catch(function (err) {
            console.log("Error", err);
        })
    }

    render() {
        return (
            <div>
                <div className="name">
                    <h2>
                        { this.state.objects['firstname'] } { this.state.objects['lastname'] }
                    </h2>
                    <div className="email">
                        <p>Ваш email {this.state.objects['email']} </p>
                    </div>
                </div>
                <div className="friends">
                    <h3>
                        Твои друзья: { this.state.objects['friends'] }
                    </h3>
                </div>
                <div className="feed">
                    <h3>
                        <Feed friendList={ this.state.objects['friends'] } />
                    </h3>
                </div>
            </div>
        );
    }
}

class Root extends React.Component {

    render() {
        return (
            <div>
                <div className='personal'>
                    <Personal currentUserId={this.props.currentUserId} />
                </div>
            </div>
        )
    }
}