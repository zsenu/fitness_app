import { Paper, Box } from "@mui/material";

function ExerciseDashboard() {
    return (
        <Paper sx = {{ p: 2 }}>
            <Box
                sx = {{
                    height: 200,
                    backgroundColor: '#668098',
                    borderRadius: 2,
                }}
            />
        </Paper>
    );
}

export default ExerciseDashboard;