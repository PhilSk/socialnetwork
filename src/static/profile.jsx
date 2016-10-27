var config = {
    container: document.getElementById("content")
};

class Feed extends React.Component {

    state = {
        objects: []
    };

    componentWillMount() {
        let _this = this;
        fetch('/api/posts/', {credentials: 'include'}).then(function (response) {
            console.log(response);
            response.json().then(function (data) {
                console.log("Fetched posts");
                console.log(data);
                _this.setState({objects: data});
            })
        }).catch(function (err) {
            console.log("Error", err);
        });
    }

    render() {
        var postList = this.state.objects;
        var func = postList.map(
            function(item, index) {
            return(
                <div key={item.pk} >
                    <h3>{item.title}</h3>
                    <p>
                        {item.content}
                    </p>
                </div>
            )
        });
        return (
            <div>
                <h3>Посты в твоей ленте от твоих друзей</h3>
                <div className="posts">
                        {func}
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
                        <Feed />
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