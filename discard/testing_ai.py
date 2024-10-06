import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
import os
from datetime import datetime, timedelta

catalog = pd.read_csv('./space_apps_2024_seismic_detection/data/lunar/training/catalogs/apollo12_catalog_GradeA_final.csv')


def load_velocity_file(file_path):
    df = pd.read_csv(file_path)
    df['time_abs'] = pd.to_datetime(df['time_abs(%Y-%m-%dT%H:%M:%S.%f)'], format='%Y-%m-%dT%H:%M:%S.%f')
    return df

def create_labeled_windows(recording_tpl, catalog_df, window_size=10000):
    windows = []
    labels = []
    recording_file = recording_tpl[0]
    recording_df = recording_tpl[1]
    
    eq_times = catalog_df[catalog_df['filename'] == recording_file]['time_abs(%Y-%m-%dT%H:%M:%S.%f)'].values
    
    for i in range(0, len(recording_df) - window_size, window_size):
        window = recording_df['velocity(m/s)'].values[i:i + window_size]
        windows.append(window)
        
        window_start_time = recording_df.iloc[i]['time_abs(%Y-%m-%dT%H:%M:%S.%f)']
        window_end_time = recording_df.iloc[i + window_size - 1]['time_abs(%Y-%m-%dT%H:%M:%S.%f)']
        
        earthquake_in_window = any([window_start_time <= eq_time <= window_end_time for eq_time in eq_times])
        labels.append(1 if earthquake_in_window else 0)
    
    return np.array(windows), np.array(labels)

def load_all_velocity_files(recording_dir):
    recordings = []
    for file in os.listdir(recording_dir):
        if file.endswith('.csv'):
            recordings.append([file[:-4], load_velocity_file(os.path.join(recording_dir, file))])
    return recordings

def extract_features_and_labels(recordings, catalog, window_size=4000):
    all_windows = []
    all_labels = []
    
    for recording_df in recordings:
        windows, labels = create_labeled_windows(recording_df, catalog, window_size)
        all_windows.append(windows)
        all_labels.append(labels)
    
    return np.concatenate(all_windows), np.concatenate(all_labels)

recording_dir = './space_apps_2024_seismic_detection/data/lunar/training/data/S12_GradeA'
recordings = load_all_velocity_files(recording_dir)

X, y = extract_features_and_labels(recordings, catalog)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=42)

clf = RandomForestClassifier(class_weight='balanced', max_depth=100, max_features='sqrt', n_estimators=200)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# save model for later use
# import pickle
# with open('earthquake_model.pkl', 'wb') as f:
#     pickle.dump(clf, f)



# param_grid = {
#     'n_estimators': [100, 200, 500],
#     'max_depth': [10, 20, 50, None],
#     'max_features': ['auto', 'sqrt', 'log2']
# }

# grid_search = GridSearchCV(estimator=clf, param_grid=param_grid, cv=5)
# grid_search.fit(X_train, y_train)

# print("Best parameters found: ", grid_search.best_params_)
