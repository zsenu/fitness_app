import { Paper, Box } from "@mui/material";

function FoodDashboard() {
    return (
        <Paper sx = {{ p: 2 }}>
            <Box
                sx = {{
                    height: 200,
                    backgroundColor: '#987d66',
                    borderRadius: 2,
                }}
            />
        </Paper>
    );
}

export default FoodDashboard;