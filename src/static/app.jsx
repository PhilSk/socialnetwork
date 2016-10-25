var config = {
    container: document.getElementsByClassName('b-wall')[0],
};

class PostList extends React.Component {

    state = {
        objects: []
    };

    loadDataFromServer() {
        let _this = this;

        fetch('/api/messages/', {credentials: 'include'})
            .then(function (response) {
                console.log(response);
                response.json().then(function (data) {
                    console.log(data);
                    _this.setState({objects:data});
                })
            })
            .catch(function (err) {
                console.log("Error", err);
            })
    }

    render() {
        return(
            <div>
                {this.state.objects.map((item) => {
                    return(<p key={item.pk}>{item.text}</p>)
                })}
                <button onClick={this.loadDataFromServer.bind(this)}>Do it!</button>
            </div>
        )
    }
}

class Root extends React.Component {
    render() {

        return (
            <div>
                <PostList/>
            </div>
        )
    }
}

ReactDOM.render(<Root />, config.container);
