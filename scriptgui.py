import PySimpleGUI as sg

def function_selector():
    # Define the layout for the GUI
    layout = [
        [sg.Text('Select the functions to enable:')],
        [sg.Checkbox('Minimization', key='Minimization'), sg.Checkbox('Docking', key='Docking'), sg.Checkbox('AlphaFold', key='AlphaFold')],
        [sg.Frame('Minimization', layout=[
            [sg.Text('Directory for Ligands:'), sg.Input(key='min_ligand_dir'), sg.FolderBrowse()],
            [sg.Text('Number of steps:'), sg.Input(key='min_num_steps', size=(5, 1))],
        ], visible=True, key='minimization_frame')],
        [sg.Frame('Docking', layout=[
            [sg.Text('Directory for Ligands:'), sg.Input(key='dock_ligand_dir'), sg.FolderBrowse()],
            [sg.Text('Directory for Receptors:'), sg.Input(key='dock_receptor_dir'), sg.FolderBrowse()],
            [sg.Text('Directory for AutoDock Vina:'), sg.Input(key='dock_autodock_dir'), sg.FolderBrowse()],
            [sg.Text('Output directory:'), sg.Input(key='dock_output_dir'), sg.FolderBrowse()],
        ], visible=True, key='docking_frame')],
        [sg.Frame('AlphaFold', layout=[
            [sg.Text('Directory for amino acid sequences:'), sg.Input(key='af_aa_dir'), sg.FolderBrowse()],
            [sg.Text('Output directory:'), sg.Input(key='af_output_dir'), sg.FolderBrowse()],
        ], visible=True, key='alphafold_frame')],
        [sg.Button('Run'), sg.Button('Exit')],
    ]

    # Create the GUI window
    window = sg.Window('Function Selector', layout)

    # Event loop
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        if event == 'Run':
            selected_functions = [func for func in ['Minimization', 'Docking', 'AlphaFold'] if values.get(func)]
            directories = {
                'min_ligand_dir': values.get('min_ligand_dir'),
                'min_num_steps': values.get('min_num_steps'),
                'dock_ligand_dir': values.get('dock_ligand_dir'),
                'dock_receptor_dir': values.get('dock_receptor_dir'),
                'dock_autodock_dir': values.get('dock_autodock_dir'),
                'dock_output_dir': values.get('dock_output_dir'),
                'af_aa_dir': values.get('af_aa_dir'),
                'af_output_dir': values.get('af_output_dir')
            }
            window.close()
            return selected_functions, directories

    window.close()