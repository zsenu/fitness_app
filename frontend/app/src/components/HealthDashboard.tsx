import { Paper, Box } from "@mui/material";

function HealthDashboard() {
    return (
        <Paper sx = {{ p: 2 }}>
            <Box
                sx = {{
                    height: 200,
                    backgroundColor: '#986698',
                    borderRadius: 2,
                }}
            />
        </Paper>
    );
}

export default HealthDashboard;