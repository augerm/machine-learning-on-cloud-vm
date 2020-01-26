params = {
    'DATA_SIZE': 120000,
    'EPOCHS': 20,
    'BATCH_SIZE': 100,
    'VALIDATION_SPLIT': .25,
    'OPTIMIZER': 'rmsprop',
    'LOSS_FUNCTION': 'binary_crossentropy',
    'SHUFFLE_TRAINING_DATA': True,
    'INPUT_LAYER': {
        'TYPE': 'Dense',
        'ACTIVATION': 'sigmoid'
    },
    'HIDDEN_LAYERS': [
        {
            'TYPE': 'Dense',
            'NUM_NODES': 600,
            'ACTIVATION': 'sigmoid'
        },
        {
            'Type': 'Dense',
            'NUM_NODES': 300,
            'ACTIVATION': 'sigmoid'
        },
        {
            'Type': 'Dense',
            'NUM_NODES': 150,
            'ACTIVATION': 'sigmoid'
        },
        {
            'Type': 'Dense',
            'NUM_NODES': 75,
            'ACTIVATION': 'sigmoid'
        }
    ],
    'OUTPUT_LAYER': {
        'TYPE': 'Dense',
        'NUM_NODES': 1,
        'ACTIVATION': 'sigmoid'
    }
}