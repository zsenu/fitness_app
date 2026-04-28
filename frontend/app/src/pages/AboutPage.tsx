import { Box, Typography, Accordion, AccordionSummary, AccordionDetails, Divider } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import NavBar from '../components/NavBar';

function AboutPage() {
    return (
    <>
        <NavBar parent = 'about' />
        <Typography variant = 'h4' gutterBottom>
            About Fitness & Health
        </Typography>

        <Typography variant = 'body1' sx = {{ mb: 3 }}>
            This section gives a simple introduction to core fitness and nutrition
            concepts to help you understand how your body responds to diet,
            exercise, and recovery.
        </Typography>

        {/* DIET */}
        <Accordion>
            <AccordionSummary expandIcon = { <ExpandMoreIcon /> }>
                <Typography variant = 'h6'>Diet</Typography>
            </AccordionSummary>
            <AccordionDetails>
                <Typography variant = 'subtitle1' sx = {{ fontWeight: 600 }}>
                    Nutrients (carbs, proteins, fats)
                </Typography>
                <Typography>
                    Carbohydrates provide energy, proteins help build and repair
                    muscles, and fats support hormones and long-term energy. A balanced
                    diet includes all three.
                </Typography>

                <Typography variant = 'subtitle1' sx = {{ fontWeight: 600 }}>
                    Calorie intake
                </Typography>
                <Typography>
                    Calories measure energy. Your calorie intake is the total energy you
                    consume from food and drinks each day.
                </Typography>

                <Typography variant = 'subtitle1' sx = {{ fontWeight: 600 }}>
                    Caloric expenditure (BMR & TDEE)
                </Typography>
                <Typography>
                    Your body burns calories to stay alive (BMR), move, and exercise.
                    Total Daily Energy Expenditure (TDEE) is the total amount you burn
                    in a day.
                </Typography>

                <Typography variant = 'subtitle1' sx = {{ fontWeight: 600 }}>
                    Weight balance (deficit vs surplus)
                </Typography>
                <Typography>
                    Body weight changes based on energy balance. Eating more than you
                    burn leads to weight gain (surplus), while eating less leads to
                    weight loss (deficit).
                </Typography>

                <Typography variant = 'subtitle1' sx = {{ fontWeight: 600 }}>
                    General diet tips
                </Typography>
                <Typography>
                    • Eat regular meals
                    <br />• Include a variety of foods
                    <br />• Focus on whole, minimally processed foods
                    <br />• Consistency matters more than perfection
                    <br />• Listen to hunger and fullness signals
                </Typography>
            </AccordionDetails>
        </Accordion>

        <Divider sx = {{ my: 2 }} />

        {/* EXERCISE */}
        <Accordion>
            <AccordionSummary expandIcon = { <ExpandMoreIcon /> }>
                <Typography variant = 'h6'>Exercise</Typography>
            </AccordionSummary>
            <AccordionDetails>
                <Typography variant = 'subtitle1' sx = {{ fontWeight: 600 }}>
                    Cardio
                </Typography>
                <Typography>
                    Cardio exercises like running or cycling improve stamina, heart
                    health, and help burn calories.
                </Typography>

                <Typography variant = 'subtitle1' sx = {{ fontWeight: 600 }}>
                    Strength training
                </Typography>
                <Typography>
                    Strength exercises build muscle and increase strength. They also
                    support long-term metabolism and body composition.
                </Typography>

                <Typography variant = 'subtitle1' sx = {{ fontWeight: 600 }}>
                    Hypertrophy & progressive overload
                </Typography>
                <Typography>
                    Muscle growth (hypertrophy) happens when muscles are challenged and
                    recover. Progress comes from gradually increasing difficulty over
                    time (progressive overload).
                </Typography>

                <Typography variant = 'subtitle1' sx = {{ fontWeight: 600 }}>
                    Rest & recovery
                </Typography>
                <Typography>
                    • Rest days prevent injury and support growth
                    <br />• Sleep is essential for recovery and performance
                    <br />• Training without recovery slows progress
                </Typography>
            </AccordionDetails>
        </Accordion>

        <Divider sx = {{ my: 2 }} />

        {/* GENERAL HEALTH */}
        <Accordion>
            <AccordionSummary expandIcon = { <ExpandMoreIcon /> }>
                <Typography variant = 'h6'>General Health</Typography>
            </AccordionSummary>
            <AccordionDetails>
                <Typography variant = 'subtitle1' sx = {{ fontWeight: 600 }}>
                    Sleep
                </Typography>
                <Typography>
                    Most adults need 7-9 hours of sleep per night for proper recovery,
                    energy, and mental focus.
                </Typography>

                <Typography variant = 'subtitle1' sx = {{ fontWeight: 600 }}>
                    Water intake
                </Typography>
                <Typography>
                    Staying hydrated supports energy, digestion, and performance.
                    Aim for around 2-3 liters per day, adjusting based on activity and
                    environment.
                </Typography>
            </AccordionDetails>
        </Accordion>
    </>
    );
};

export default AboutPage;
