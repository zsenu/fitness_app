import ageCalculator from './ageCalculator';

const bmrTdeeCalculator = (gender: string, birthDate: string, weight: number, height: number, activityLevel: string): { bmr: number, tdee: number } => {

    const age = ageCalculator(birthDate);
    let bmr: number;
    if (gender === 'M') {
        bmr = 10 * weight + 6.25 * height - 5 * age + 5;
    }
    else {
        bmr = 10 * weight + 6.25 * height - 5 * age - 161;
    }

    let activityMultiplier: number;
    switch (activityLevel) {
        case 'sedentary':
            activityMultiplier = 1.2;
            break;
        case 'lightly_active':
            activityMultiplier = 1.375;
            break;
        case 'moderately_active':
            activityMultiplier = 1.55;
            break;
        case 'very_active':
            activityMultiplier = 1.725;
            break;
        case 'extra_active':
            activityMultiplier = 1.9;
            break;
        default:
            activityMultiplier = 1.2;
    }

    const tdee = bmr * activityMultiplier;

    return { bmr: Math.round(bmr), tdee: Math.round(tdee) };
}

export default bmrTdeeCalculator;
