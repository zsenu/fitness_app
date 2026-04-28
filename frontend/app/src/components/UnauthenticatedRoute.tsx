import { Navigate } from "react-router-dom";
import { useSelector } from "react-redux";
import type { RootState } from "../store/store";

type Props = {
    children: React.ReactNode;
};

function UnauthenticatedRoute({ children }: Props) {
    const isAuthenticated = useSelector(
        (state: RootState) => state.auth.isAuthenticated
    );

    if (isAuthenticated) {
        return <Navigate to = '/dashboard' replace />;
    }

    return children;
}

export default UnauthenticatedRoute;
