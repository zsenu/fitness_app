import { AppBar, Toolbar, Button, Stack } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import type { RootState, AppDispatch } from '../store/store';
import { logout } from '../store/thunks/authThunk';

function NavBar({ parent }: { parent: string | null }) {

    const isAuthenticated = useSelector((state: RootState) => state.auth.isAuthenticated);
    const navigate = useNavigate();
    const dispatch = useDispatch<AppDispatch>();

    const handleLogout = () => {
        dispatch(logout());
        navigate('/');
    }
    
    return(
    <AppBar position = 'sticky'
            sx={{ top: 0, left: 0, width: '100%', margin: 0, padding: 0 }}
    >
        <Toolbar>
            <Stack direction = 'row' spacing = { 1 }>
                {
                    parent !== 'about' &&
                    <Button color = 'inherit' onClick = {() => { navigate('/about'); }}>
                        About
                    </Button>
                }
                {
                    isAuthenticated && parent !== 'dashboard' &&
                    <Button color = 'inherit' onClick = {() => { navigate('/dashboard'); }}>
                        Dashboard
                    </Button>
                }
                {
                    isAuthenticated && parent !== 'profile' &&
                    <Button color = 'inherit' onClick = {() => { navigate('/profile'); }}>
                        Profile
                    </Button>
                }
                {
                    isAuthenticated ?
                    <Button color = 'inherit' onClick = { handleLogout }>
                        Sign Out
                    </Button>
                    :
                    <Button color = 'inherit' onClick = {() => { navigate('/'); }}>
                        Sign In
                    </Button>
                }
            </Stack>
        </Toolbar>
    </AppBar>
    );
};

export default NavBar;