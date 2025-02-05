import * as React from 'react';
import { Component } from 'react';
import {UserData} from "../api/user";
import {DEFAULT_AVATAR} from '../util/user-view'


interface Props {
    user: UserData
}

interface State {
    isOpen: boolean
}


class PageLoginStatus extends Component<Props, State> {
    state: State = {
        isOpen: false
    };

    menuRef: any = null;

    componentDidMount() {
        window.addEventListener('click', this.onPageClick);
    }

    componentWillUnmount() {
        window.removeEventListener('click', this.onPageClick);
    }

    onPageClick = (e) => {
        let p = e.target;
        while (p) {
            if (p === this.menuRef) {
                return;
            }
            p = p.parentNode;
        }
        this.setState({ isOpen: false });
    };

    toggleMenu = (e) => {
        e.preventDefault();
        e.stopPropagation();

        this.setState({ isOpen: !this.state.isOpen });
    };

    render() {
        const { user } = this.props;
        const { isOpen } = this.state;

        if (user.type === 'anonymous') {
            return (
                <>
                    <a className="login-status-create-account btn" href="/system:join">Создать учётную запись</a> <span>или</span> <a className="login-status-sign-in btn btn-primary" href={`/-/login?to=${encodeURIComponent(window.location.href)}`}>Вход</a>
                </>
            );
        } else {
            return (
                <>
                    <span className="printuser w-user">
                        <a href={`/-/profile`}>
                            <img className="small" src={user.avatar || DEFAULT_AVATAR} alt={user.username} />
                        </a>
                        {user.username}
                    </span>{
                    (user.admin || user.staff) && (
                        <>
                            {'\u00a0'}|{'\u00a0'}<a id="w-admin-link" href={`/-/admin`}>
                            Админ-панель
                        </a>
                        </>
                    )}{'\u00a0|\u00a0'}<a id="my-account" href={`/-/users/${user.id}-${user.username}`}>
                        Мой профиль
                    </a>
                    <a id="account-topbutton" href="#" onClick={this.toggleMenu}>▼</a>
                    { isOpen && <div id="account-options" ref={r => this.menuRef = r} style={{ display: 'block' }}>
                        <ul>
                            <li><a href={`/-/profile/edit`}>Настройки</a></li>
                            <li><a href={`/-/logout?to=${encodeURIComponent(window.location.href)}`}>Выход</a></li>
                        </ul>
                    </div> }
                </>
            )
        }
    }

}


export default PageLoginStatus
