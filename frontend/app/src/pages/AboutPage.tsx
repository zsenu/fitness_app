import { Box, Typography, Accordion, AccordionSummary, AccordionDetails, Divider } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import NavBar from '../components/NavBar';

function AboutPage() {
    return (
    <>
    <NavBar parent = 'about' />
    <Box sx = {{ p: 2 }}>
        <Typography variant = 'h4' gutterBottom>
            About Fitness & Health
        </Typography>

        <Typography variant = 'body1' sx = {{ mb: 3 }}>
            When it comes to fitness and health, there's a lot to learn. Understanding
            the key aspects can help you achieve better results, faster. Here you can find
            short introductions to each core aspect. Note: this is not a scientific article.
            Please research the topics you're interested in.
        </Typography>

        {/* DIET */}
        <Accordion>
            <AccordionSummary expandIcon = { <ExpandMoreIcon /> }>
                <Typography variant = 'h6'>Diet</Typography>
            </AccordionSummary>
            <AccordionDetails>
                <Typography variant = 'subtitle1' sx = {{ fontWeight: 600, marginBottom: 2, marginTop: 1 }}>
                    What are calories?
                </Typography>
                <Typography>
                    A calorie is a measure of energy. Your body uses a lot of energy
                    every day, to heat itself up, to circulate blood, move your legs, digest food,
                    <br />
                    The exact amount of energy your body needs in order to survive is called the <strong>Basal Metabolic Rate (BMR)</strong>.
                    It's influenced by many factors, including your gender, age, height and bodyweight.
                    <br />
                    However, there's more than survival. Depending on your lifestyle and activity level, you need extra energy to facilitate your daily tasks.
                    Your <strong>Total Daily Energy Expenditure (TDEE)</strong> measures this total. Even if you're just sitting most of the time,
                    up to 20% extra calories might be needed, just to do this.
                </Typography>
                <Typography variant = 'subtitle1' sx = {{ fontWeight: 600, marginBottom: 2, marginTop: 1 }}>
                    What do calories have to do with your weight?
                </Typography>
                <Typography>
                    When your body receives a surplus of calories, and it has nothing to do with it, its evolutionary instinct is to store as much of it as possible.
                    The most efficient way of storing this extra energy is in the form of fat.
                    When you eat more calories than you need it's called a <strong>caloric surplus</strong>.
                    <br />
                    On the other side, if there's insufficient energy provided, your body resorts to your reserves. This mainly includes the extra fat it stored previously,
                    but in extreme cases your body can break down your muscles and even suspend important functions within your body (like your immune system).
                    When you eat less calories than you need it's called a <strong>caloric deficit</strong>.
                </Typography>
                <Typography variant = 'subtitle1' sx = {{ fontWeight: 600, marginBottom: 2, marginTop: 1 }}>
                    How to change your bodyweight
                </Typography>
                <Typography>
                    A kilogram of fat contains roughly <strong>7700 calories</strong>. So, accumulating a caloric surplus of this amount results in gaining roughly 1 kilogram of fat.
                    Accumulating a caloric deficit of 7700 calories over time makes your body metabolize around a kilogram of fat from your body.
                    <br />
                    Please note that these are long processes. A daily caloric intake that deviates more than ~30% from your TDEE is often considered dangerous. Your body changes slowly,
                    slow and steady is the recommended way.
                </Typography>
                <Typography variant = 'subtitle1' sx = {{ fontWeight: 600, marginBottom: 2, marginTop: 1 }}>
                    Macronutrients
                </Typography>
                <Typography>
                    The things you consume are made up of many components, but three very important components are <strong>carbohydrates, fats and proteins</strong>.
                    <br />
                    <strong>Carbohydrates</strong> (carbs for short) are the most easily metabolizable energy source for your body.
                    Your body transports energy around your body via sugars.
                    <br />
                    <strong>Fats</strong> are more concentrated sources of energy. They serve an important role in your body's hormone production. Healthy, unprocessed fats are part of a good diet.
                    <br />
                    <strong>Proteins</strong> are the building blocks of your body. Their main use is in repairing and building muscle tissue.
                </Typography>

                <Typography variant = 'subtitle1' sx = {{ fontWeight: 600, marginBottom: 2, marginTop: 1 }}>
                    General tips for a healthy diet
                </Typography>
                <Typography>
                    • Regularly eat meals through the day
                    <br />
                    • Prioritize whole, unprocessed foods
                    <br />
                    • Diversify your meals, eat different types of foods
                    <br />
                    • Allow time for fullness signals to register
                    <br />
                    • Self-starvation is generally a bad idea
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
                <Typography variant = 'subtitle1' sx = {{ fontWeight: 600, marginBottom: 2, marginTop: 1 }}>
                    Cardio training
                </Typography>
                <Typography>
                    Deriving from the greek word "kardía" (= heart), cardio exercises generally aim to elevate your heartrate
                    for an extended period of time. This can improve your cardiovascular health (heart muscles), your stamina,
                    and the high heartrate increases the calories burned per minute.
                    <br />
                    As with everything else, moderation is important here. Don't push yourself to dangerous extents.
                </Typography>

                <Typography variant = 'subtitle1' sx = {{ fontWeight: 600, marginBottom: 2, marginTop: 1 }}>
                    Strength training
                </Typography>
                <Typography>
                    Strength exercises involve some sort of resistance that your muscles have to work against.
                    The resistance can be a foreign object or even your own bodyweight.
                    Strength training can result in an increased muscle mass and greater strength.
                </Typography>

                <Typography variant = 'subtitle1' sx = {{ fontWeight: 600, marginBottom: 2, marginTop: 1 }}>
                    How to build muscles?
                </Typography>
                <Typography>
                    The process of muscle growth is called <strong>hypertrophy</strong>. When your muscles are challenged, micro-tears appear on them.
                    If proper muscle stimulation and <strong>excess nutrients</strong> (calories and protein) are provided, your body doesn't just regenerate them,
                    it increases their volume.
                    <br />
                    As your muscles adapt to the increased workload, the old routines may not challenge them enough to trigger muscle growth.
                    To solve this, gradually increase the workload (by increasing weights, sets or reps, or even just doing exercises in a slow, concentrated manner)
                    that your muscles have to bear. This is called <strong>progressive overloading</strong>.
                </Typography>

                <Typography variant = 'subtitle1' sx = {{ fontWeight: 600, marginBottom: 2, marginTop: 1 }}>
                    Rest & recovery
                </Typography>
                <Typography>
                    Putting your body under this increased strain means that it will need time to recover. Cell regeneration and muscle building is most efficient during sleep.
                    <br />
                    Besides adequate sleep, it is recommended to take <strong>break days</strong> in order to let your body properly regenerate.
                    Overworking yourself may slow your progress down.
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
                <Typography variant = 'subtitle1' sx = {{ fontWeight: 600, marginBottom: 2, marginTop: 1 }}>
                    Sleep
                </Typography>
                <Typography>
                    Many important processes within your body happen during sleep. The recommended amount of sleep for an adult is around 7-8 hours.
                    <br />
                    Try to have a consistent bedtime and wake-up time. A healthy sleep schedule can lead to better energy levels, better focus and mood.
                </Typography>

                <Typography variant = 'subtitle1' sx = {{ fontWeight: 600, marginBottom: 2, marginTop: 1 }}>
                    Water intake
                </Typography>
                <Typography>
                    Consuming an adequate amount of water each day is very important. The recommended amount of liquid intake for an adult is around 2-3 liters.
                    <br />
                    Prioritize water and organic teas. Substances like caffeine and alcohol dehydrate the body, so make sure to account for that.
                    <br />
                    Based on your body, lifestyle and environment, you may need an increased amount of water. Don't stay thirsty!
                </Typography>
            </AccordionDetails>
        </Accordion>
    </Box>
    </>
    );
};

export default AboutPage;
