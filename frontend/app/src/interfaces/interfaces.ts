export interface ErrorResponse {
    detail: string;
};

export interface ValidationErrorResponse {
    [field : string]: string[];
};

export interface AuthState {
    isAuthenticated: boolean;
    userProfile:     ProfileDataType | null;
    accessToken:     string | null;
    loading:         boolean;
    error:           ValidationErrorResponse | string | null;
};

export interface LoginDataType {
    username: string;
    password: string;
};

export interface RegisterDataType {
    username:        string;
    password:        string;
    password2:       string;
    email:           string;
    gender:          string;
    birth_date:      string;
    height:          number;
    starting_weight: number;
    activity_level:  string;
    target_weight:   number;
    target_date:     string;
    target_calories: number;
};

export interface ProfileDataType {
    id:              number;
    username:        string;
    email:           string;
    gender:          string;
    birth_date:      string;
    height:          number;
    starting_weight: number;
    current_weight:  number;
    activity_level:  string;
    target_weight:   number;
    target_date:     string;
    target_calories: number;
    bmr:             number;
    tdee:            number;
};

export interface DashboardState {
    activeDate: string;
};

export interface HealthLogType {
    id: number;
    date: string;
    bodyweight: number | null;
    hours_slept: number | null;
    liquid_consumed: number | null;
};

export interface HealthLogState {
    activeLog: HealthLogType | null;
    loading: boolean;
    error: ValidationErrorResponse | null;
};

export interface HealthLogUpdatePayload {
    id: number;
    data: Partial<Pick<HealthLogType,
        'bodyweight' | 'hours_slept' | 'liquid_consumed'
    >>;
};

export interface FoodItemType {
    id: number;
    name: string;
    description: string;
    calories: string;
    fat: string;
    carbohydrates: string;
    protein: string;
};

export interface FoodItemState {
    foodItems: FoodItemType[];
    loading: boolean;
    error: ValidationErrorResponse | null;
}

export interface FoodEntryType {
    id: number;
    parent_log: number;
    meal_type: 'breakfast' | 'lunch' | 'dinner' | 'misc';
    food_item: FoodItemType;
    quantity: string;
    description: string;
};

export interface FoodEntryPayloadType {
    meal_type: 'breakfast' | 'lunch' | 'dinner' | 'misc';
    food_item_id: number;
    quantity: string;
    description: string;
}

export interface MacrosType {
    calories: number;
    fat: number;
    carbohydrates: number;
    protein: number;
};

export interface FoodLogType {
    id: number;
    date: string;
    entries: FoodEntryType[];

    breakfast_macros: MacrosType;
    lunch_macros: MacrosType;
    dinner_macros: MacrosType;
    misc_macros: MacrosType;
    total_macros: MacrosType;
};

export interface FoodLogState {
    activeLog: FoodLogType | null;
    loading: boolean;
    error: ValidationErrorResponse | null;
};

export type MealType = FoodEntryType['meal_type'];
