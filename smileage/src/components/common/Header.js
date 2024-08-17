import styles from 'styles/Header.module.css';

function Header() {
    return (
        <>
            <header className={styles.header}>
                <img src="/logo_rot.png" alt="logo" className={styles.logo} />
            </header>
        </>
    )
}

export default Header;
