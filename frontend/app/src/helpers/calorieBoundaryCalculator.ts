import bmrTdeeCalculator from './bmrTdeeCalculator';

const calorieBoundaryCalculator = (gender: string, birthDate: string, weight: number, height: number, activityLevel: string) : { minCalories: number, maxCalories: number } => {

    const tdee: number = bmrTdeeCalculator(gender, birthDate, weight, height, activityLevel).tdee;

    return {
        minCalories: Math.max(Math.round(tdee * 0.65), gender === 'M' ? 1500 : 1200),
        maxCalories: Math.round(tdee * 1.35)
    };
}

export default calorieBoundaryCalculator;
