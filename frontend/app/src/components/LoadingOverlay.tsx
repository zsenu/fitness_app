import { useSelector } from 'react-redux';
import type { RootState } from '../store/store';
import { selectIsGlobalLoading } from '../store/selectors';

const LoadingOverlay = () => {

    const isLoading = useSelector((state: RootState) => selectIsGlobalLoading(state));

    if (!isLoading) return null;

    return (
        <div style = {{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100vw',
            height: '100vh',
            background: 'rgba(0,0,0,0.4)',
            backdropFilter: 'blur(4px)',
            color: '#ffffff',
            fontSize: '1.5rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 9999
        }}>
            <div>Loading...</div>
        </div>
    );
};

export default LoadingOverlay;