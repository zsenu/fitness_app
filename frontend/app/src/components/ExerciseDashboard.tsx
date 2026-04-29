import { Box } from "@mui/material";

function ExerciseDashboard() {
    return (
        <Box
            sx = {{
                padding: 2,
                height: 300,
                backgroundColor: '#94b6d6',
                borderRadius: 2
            }}
        >
                    <Box
            sx = {{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 18,
                fontWeight: 'bold'
            }}
        >
            Exercise Log
        </Box>
        </Box>
    );
}

export default ExerciseDashboard;