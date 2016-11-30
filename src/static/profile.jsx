var config = {
    container: document.getElementById("content")
};

class Feed extends React.Component {

    state = {
        objects: []
    };

    componentWillMount() {
        let _this = this;
        fetch('/api/events/', {credentials: 'include'}).then(function (response) {
            console.log(response);
            response.json().then(function (data) {
                console.log("Fetched events");
                console.log(data);
                _this.setState({objects: data});
            })
        }).catch(function (err) {
            console.log("Error", err);
        });
    }

    render() {
        var eventList = this.state.objects;
        var show_events = eventList.map(
            function(item, index) {
            return(
                <li key={item.pk} >
                    {item.name}
                </li>
            )
        });
        return (
            <div>
                <h2 className="h1">Лента</h2>
                <div className="events">
                    <ul>
                        {show_events}
                    </ul>
                </div>
            </div>
        );
    }
}

class Personal extends React.Component {

    state = {
        currentUserId: this.props.currentUserId,
        objects: []
    };

    componentWillMount() {
        let _this = this;

        fetch('/api/users/' + this.state.currentUserId + '/', {credentials: 'include'}).then(function (response) {
            console.log(response);
            response.json().then(function (data) {
                console.log("Fetched users");
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
                <div className="col-xs-4">
                    <div className="name">
                        <h1>
                            { this.state.objects['firstname'] } { this.state.objects['lastname'] }
                        </h1>
                        <div className="email">
                            <p>Ваш email {this.state.objects['email']} </p>
                        </div>
                    </div>
                    <div className="friends">
                        <h3>
                            Твои друзья: {this.state.objects['friendships']}
                        </h3>
                    </div>
                </div>
                <div className="col-xs-8">
                    <div className="feed">
                        <h3>
                            <Feed />
                        </h3>
                    </div>
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