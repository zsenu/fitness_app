import { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import type { RootState } from '../store/store';
import { Container, Paper, Typography, CircularProgress } from '@mui/material';
import type { StatisticsDataType } from '../interfaces/interfaces';

function StatisticsContainer() {
    const [statistics, setStatistics] = useState<StatisticsDataType | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    const authToken = useSelector((state: RootState) => state.auth.accessToken);

    useEffect(() => {
        const fetchStatistics = async () => {
            try {
                setLoading(true);
                setError(null);

                const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/statistics/`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${ authToken }`
                    }
                });

                if (!response.ok) {
                    throw new Error(`Error: ${response.statusText}`);
                }

                const data = await response.json();
                setStatistics(data);
            } catch (err: unknown) {
                if (err instanceof Error) {
                    setError(err.message);
                }
                else {
                    setError('An unknown error occurred');
                }
            } finally {
                setLoading(false);
            }
        };

        fetchStatistics();
    }, [authToken]);

    const [elapsedDaysText, setElapsedDaysText] = useState<string>('');
    const [weightChangeText, setWeightChangeText] = useState<string>('');
    const [strengthTrainingText, setStrengthTrainingText] = useState<string>('');
    const [cardioTrainingText, setCardioTrainingText] = useState<string>('');
    const [foodLogText, setFoodLogText] = useState<string>('');
    const [healthLogText, setHealthLogText] = useState<string>('');

    const elapsedWeeks = statistics ? statistics.elapsed_days / 7 : 0;
    const weeklyWeightChange = statistics ? statistics.weight_difference / elapsedWeeks : 0;

    useEffect(() => {
        if (statistics) {
            setElapsedDaysText(`Elapsed days since joining: ${ statistics.elapsed_days }`);
            setWeightChangeText(`Weight change: ${ statistics.weight_difference > 0 ? 'gained ' : 'lost ' }${ Math.abs(statistics.weight_difference) } kg (${ weeklyWeightChange > 0 ? 'gained ' : 'lost ' }${ Math.abs(weeklyWeightChange).toFixed(2) } kg/week)`);
            setStrengthTrainingText(`Strength training sessions recorded: ${ statistics.strength_training_count }`);
            setCardioTrainingText(`Cardio training sessions recorded: ${ statistics.cardio_training_count }`);
            setFoodLogText(`Food logs recorded: ${ statistics.food_log_count }`);
            setHealthLogText(`Health logs recorded: ${ statistics.health_log_count }`);
        }
    }, [statistics]);
    
    return (
    <Container maxWidth = 'sm' sx = {{ mt: 6 }}>
        <Paper sx = {{ p: 4 }}>
            <Typography variant = 'h4' gutterBottom>
                Statistics
            </Typography>
        
            { loading && <CircularProgress /> }
            { error && (
                <Typography variant = 'body1' color = 'error'>
                    { error }
                </Typography>
            )}
            {statistics && (
                <Typography variant = 'body1'>
                    { elapsedDaysText }<br />
                    { weightChangeText }<br />
                    { strengthTrainingText }<br />
                    { cardioTrainingText }<br />
                    { foodLogText }<br />
                    { healthLogText }
                </Typography>
            )}
        </Paper>
    </Container>
    );
};

export default StatisticsContainer;
