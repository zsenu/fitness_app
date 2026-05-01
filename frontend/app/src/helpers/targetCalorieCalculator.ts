import bmrTdeeCalculator from './bmrTdeeCalculator';

const targetCalorieCalculator = (gender: string, birthDate: string, weight: number, height: number, activityLevel: string, targetWeight: number, targetDate: string): number => {

    const tdee : number = bmrTdeeCalculator(gender, birthDate, weight, height, activityLevel).tdee;

    const weightDifference = targetWeight - weight;

    if (weightDifference === 0) {
        return tdee;
    }

    const daysUntilTarget = Math.max(1, Math.ceil((new Date(targetDate).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24)));
    const dailyCalorieChange = (weightDifference * 7700) / daysUntilTarget;

    return Math.round(tdee + dailyCalorieChange);
}

export default targetCalorieCalculator;
