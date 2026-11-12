import sqlite3

def initial_database():
    conn = sqlite3.connect('errorease.db')
    cursor = conn.cursor()

    # Enable foreign key enforcement
    cursor.execute('PRAGMA foreign_keys = ON')

    # Creating table with errors including possible multiple solutions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SOLUTIONS (
            SolutionID INTEGER PRIMARY KEY AUTOINCREMENT,
            ErrorCode TEXT NOT NULL,
            PlainEnglishSummary TEXT,
            StepByStepFix TEXT,
            Upvotes INTEGER DEFAULT 0,
            Downvotes INTEGER DEFAULT 0,

            FOREIGN KEY (ErrorCode)
                REFERENCES ERRORS(ErrorCode)
        )
    ''')
    #Creating errors table to store error codes and their descriptions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ERRORS (
            ErrorCode TEXT PRIMARY KEY,
            ErrorName TEXT,
            ErrorDescription TEXT
        )
    ''')
    # Format: (ErrorCode, Summary, 3-Step Fix, Upvotes, Downvotes)
    initial_solutions_data = [
        ('0x80070005', 'Access Denied (Permission Error)', '1. Right-click the trusted program or installer.\n2. Select "Run as administrator" if the program needs it.\n3. Try the same action again.', 0, 0),
        ('0x80070005', 'Access Denied (Permission Error)', '1. Find the file or folder mentioned in the error.\n2. Right-click it and open Properties > Security.\n3. Check whether your account has the needed permission. Do not change Windows system permissions without identifying the problem.', 0, 0),
        ('0x80070005', 'Access Denied (Permission Error)', '1. Open Windows Security > Protection history.\n2. Check whether a security warning matches the time of the error.\n3. If a trusted program was blocked by mistake, review that specific warning rather than turning off antivirus protection.', 0, 0),
        ('0x80070002', 'Required File Not Found', "1. Check the file name or path shown in the error.\n2. Make sure the file exists and has not been moved or deleted.\n3. If it belongs to an application, use that application's Repair option or reinstall it from its official source.", 0, 0),
        ('0x80070002', 'Required File Not Found', '1. If this happened during Windows Update, restart your PC.\n2. Open Settings > System > Troubleshoot > Other troubleshooters.\n3. Run Windows Update troubleshooter and try the update again.', 0, 0),
        ('0x80070002', 'Required File Not Found', '1. If Windows Update still fails, open Settings > Windows Update > Update history.\n2. Find the update that failed and write down its KB number.\n3. Look up the KB on Microsoft Support and follow its specific repair instructions.', 0, 0),
        ('0x80073D05', 'Microsoft Store App Data Could Not Be Deleted', "1. Close the affected Microsoft Store app.\n2. Close any editor, simulator, or other program using the app's files.\n3. Try installing or updating the app again.", 0, 0),
        ('0x80073D05', 'Microsoft Store App Data Could Not Be Deleted', '1. Save your work and restart your PC.\n2. Do not open the affected app after restarting.\n3. Try installing or updating the app again.', 0, 0),
        ('0x80073D05', 'Microsoft Store App Data Could Not Be Deleted', '1. Open Event Viewer from the Start menu.\n2. Go to Applications and Services Logs > Microsoft > Windows > AppXDeployment-Server > Operational.\n3. Check the error at the install time to find the app file or process blocking the operation.', 0, 0),
        ('0x800704CF', 'Network Location Cannot Be Reached', '1. Make sure Wi-Fi or Ethernet is connected.\n2. Try opening a website to test your connection.\n3. If you are accessing a shared folder or server, check its network address and try again.', 0, 0),
        ('0x800704CF', 'Network Location Cannot Be Reached', '1. If the resource needs a VPN, connect to the required VPN.\n2. Check whether the server is reachable from that network.\n3. Ask the network administrator for help if the server still cannot be reached.', 0, 0),
        ('0x800704CF', 'Network Location Cannot Be Reached', "1. Open Settings > Network & internet.\n2. Check for an incorrect proxy or disconnected network adapter.\n3. Correct the connection using your network's normal settings, then try again.", 0, 0),
        ('0x800f0922', 'Windows Update or Servicing Installation Failed', '1. Restart your computer and check that the system drive has free space.\n2. Open Settings > Windows Update and check for pending updates.\n3. Try installing the failed update again.', 0, 0),
        ('0x800f0922', 'Windows Update or Servicing Installation Failed', '1. Open Command Prompt as administrator.\n2. Run "DISM /Online /Cleanup-Image /RestoreHealth" and then "sfc /scannow" if you suspect damaged Windows files.\n3. Restart your PC and retry the failed update.', 0, 0),
        ('0x800f0922', 'Windows Update or Servicing Installation Failed', '1. Open the file C:\\Windows\\Logs\\CBS\\CBS.log.\n2. Look for 0x800f0922 near the time the installation failed.\n3. Check the package or installer named in the log before following a specific repair.', 0, 0),
        ('0x80070422', 'Required Service Is Disabled', '1. Press Win + R, type "services.msc", and press Enter.\n2. Find Windows Update and check whether its Startup type is Disabled.\n3. If allowed on your PC, restore its normal startup setting and try the update again.', 0, 0),
        ('0x80070422', 'Required Service Is Disabled', '1. If Windows Update cannot download files, open "services.msc".\n2. Find Background Intelligent Transfer Service (BITS) and check whether it is disabled.\n3. If it is disabled unexpectedly, restore its normal setting and retry the update.', 0, 0),
        ('0x80070422', 'Required Service Is Disabled', '1. Restart your PC.\n2. Open Settings > System > Troubleshoot > Other troubleshooters.\n3. Run the Windows Update troubleshooter and follow its instructions.', 0, 0),
        ('0xc0000005', 'Access Violation (Application Crash)', '1. Find the application that crashes.\n2. Update it from its official website or app store.\n3. Restart the application and check whether it still crashes.', 0, 0),
        ('0xc0000005', 'Access Violation (Application Crash)', '1. Disable optional plugins, add-ons, or overlays for that application.\n2. Try launching it with the default settings.\n3. If it works, turn the extras back on one at a time to find the problem.', 0, 0),
        ('0xc0000005', 'Access Violation (Application Crash)', '1. Press Win + R, type "eventvwr.msc", and press Enter.\n2. Open Windows Logs > Application and find the crash.\n3. Note the Faulting module name and use it to look for an app- or driver-specific fix.', 0, 0),
        ('0x80070057', 'Invalid Parameter (Incorrect Value)', '1. Check the values and options used when the error appeared.\n2. Make sure any file path, drive selection, or setting is valid.\n3. Try the operation again with the corrected value.', 0, 0),
        ('0x80070057', 'Invalid Parameter (Incorrect Value)', '1. If this happened during Windows Update, restart your PC.\n2. Open Settings > System > Troubleshoot > Other troubleshooters.\n3. Run Windows Update troubleshooter and retry the update.', 0, 0),
        ('0x80070057', 'Invalid Parameter (Incorrect Value)', '1. If Windows files may be damaged, open Command Prompt as administrator.\n2. Run "DISM /Online /Cleanup-Image /RestoreHealth" and then "sfc /scannow".\n3. Restart your PC and try again. This repair is for Windows file problems, not every invalid parameter.', 0, 0),
        ('0x80070003', 'Required Folder or Path Not Found', '1. Check the folder path shown in the error.\n2. Make sure the folder exists and is spelled correctly.\n3. Reconnect a USB or network drive if the missing path points to one.', 0, 0),
        ('0x80070003', 'Required Folder or Path Not Found', '1. If this happened during Windows Update, restart your PC.\n2. Open Settings > System > Troubleshoot > Other troubleshooters.\n3. Run the Windows Update troubleshooter and retry the update.', 0, 0),
        ('0x80070003', 'Required Folder or Path Not Found', '1. Open C:\\Windows\\Logs\\CBS\\CBS.log if a Windows update failed.\n2. Look for 0x80070003 or "path not found" near the failure time.\n3. Use the named missing path or package to decide what needs repairing.', 0, 0),
        ('0x80070490', 'Required Item Not Found (Element Not Found)', '1. Restart your computer.\n2. Open Settings > Windows Update > Update history.\n3. Retry the update that failed and note its KB number if it fails again.', 0, 0),
        ('0x80070490', 'Required Item Not Found (Element Not Found)', '1. Open C:\\Windows\\Logs\\CBS\\CBS.log.\n2. Find entries near the failure time mentioning 0x80070490.\n3. Check whether a missing driver or update component is listed before attempting a repair.', 0, 0),
        ('0x80070490', 'Required Item Not Found (Element Not Found)', "1. If the update logs identify a driver, open Device Manager.\n2. Find the affected device and check its model.\n3. Install the supported driver from the PC or device maker's official website and retry.", 0, 0),
        ('0x80080005', 'COM Server Execution Failed', '1. Restart your computer.\n2. Open the application that showed the error.\n3. Try the same action again and note whether only that application is affected.', 0, 0),
        ('0x80080005', 'COM Server Execution Failed', '1. Open Settings > Apps > Installed apps.\n2. Find the affected application and use Repair if available.\n3. If Repair is unavailable, reinstall it using the official installer.', 0, 0),
        ('0x80080005', 'COM Server Execution Failed', '1. Press Win + R, type "eventvwr.msc", and press Enter.\n2. Open Windows Logs > Application and System.\n3. Look for COM, DistributedCOM, or application errors from the same time to identify the failed component.', 0, 0),
        ('0x80240034', 'Windows Update Failed to Download', '1. Check that your internet connection works.\n2. Restart your computer.\n3. Open Settings > Windows Update and try downloading the update again.', 0, 0),
        ('0x80240034', 'Windows Update Failed to Download', '1. Open Settings > System > Troubleshoot > Other troubleshooters.\n2. Run the Windows Update troubleshooter.\n3. Follow its instructions and retry the download.', 0, 0),
        ('0x80240034', 'Windows Update Failed to Download', '1. Press Win + R, type "services.msc", and press Enter.\n2. Stop Windows Update, then delete only the contents of C:\\Windows\\SoftwareDistribution\\Download.\n3. Start Windows Update again and retry the download.', 0, 0),
        ('0x8007007e', 'Required Module or DLL Not Found', '1. Find the application that displays the error.\n2. Open Settings > Apps > Installed apps and select Repair if available.\n3. If there is no Repair option, reinstall the app from its official source.', 0, 0),
        ('0x8007007e', 'Required Module or DLL Not Found', "1. Check the application's official requirements for missing runtimes.\n2. Install any required runtime from Microsoft or the application's official website.\n3. Restart the application. Avoid downloading individual DLL files from random websites.", 0, 0),
        ('0x8007007e', 'Required Module or DLL Not Found', '1. If the missing module belongs to Windows, open Command Prompt as administrator.\n2. Run "DISM /Online /Cleanup-Image /RestoreHealth" and then "sfc /scannow".\n3. Restart your computer and try again.', 0, 0),
        ('0x80070643', 'Fatal Error During Installation', "1. Find the program or Windows update that failed.\n2. Restart your computer and try installing it again.\n3. If it still fails, check the installer log or the update's KB number for the specific cause.", 0, 0),
        ('0x80070643', 'Fatal Error During Installation', '1. If a Windows update failed, open Settings > System > Troubleshoot > Other troubleshooters.\n2. Run Windows Update troubleshooter.\n3. Restart if requested and try installing the update again.', 0, 0),
        ('0x80070643', 'Fatal Error During Installation', '1. Check whether the failed installer is specifically for .NET Framework.\n2. If it is, download the .NET Framework Repair Tool from Microsoft.\n3. Run it, restart your PC, and retry the .NET installation. Do not use this tool for unrelated installers.', 0, 0)
    ]
    # Initial error data
    initial_errors_data = [
        # (ErrorCode, ErrorName, ErrorDescription)
        ('0x80070005', 'Access Denied', 'Occurs when a user or application does not have sufficient permissions to access or modify a resource.'),
        ('0x80070002', 'Required File Not Found', 'Occurs when Windows cannot locate a required file during an operation or update.'),
        ('0x80073D05', 'Microsoft Store App Data Could Not Be Deleted', 'Occurs when Windows fails to delete or clean up application data during an app operation.'),
        ('0x800704CF', 'Network Location Cannot Be Reached', 'Occurs when Windows cannot connect to a network location or access a network resource.'),
        ('0x800f0922', 'Windows Update or Servicing Installation Failed', 'Occurs when Windows fails to install an update, often because of connectivity or system partition issues.'),
        ('0x80070422', 'Required Service Is Disabled', 'Occurs when a Windows service required for an operation is disabled or unavailable.'),
        ('0xc0000005', 'Access Violation (Application Crash)', 'Occurs when an application attempts to access an invalid or restricted memory location.'),
        ('0x80070057', 'Invalid Parameter (Incorrect Value)', 'Occurs when Windows receives an incorrect or invalid parameter during an operation.'),
        ('0x80070003', 'Required Folder or Path Not Found', 'Occurs when Windows cannot locate a specified folder or directory.'),
        ('0x80070490', 'Required Item Not Found (Element Not Found)', 'Occurs when Windows cannot find a required system component, configuration element, or update reference.'),
        ('0x80080005', 'COM Server Execution Failed', 'Occurs when Windows cannot properly start or communicate with a required COM server process.'),
        ('0x80240034', 'Windows Update Failed to Download', 'Occurs when Windows Update fails to download or complete the installation of an update.'),
        ('0x8007007e', 'Required Module or DLL Not Found', 'Occurs when Windows cannot find a required program module or dynamic-link library (DLL).'),
        ('0x80070643', 'Fatal Error During Installation','Occurs when a software installation or update fails due to a serious installation-related problem.'),
    ]

    # Insert errors if they don't already exist
    cursor.executemany('''
    INSERT OR IGNORE INTO ERRORS
    (ErrorCode, ErrorName, ErrorDescription)
    VALUES (?, ?, ?)
''', initial_errors_data)

    # Checking if there's already file exist
    cursor.executemany('''
        INSERT INTO SOLUTIONS (ErrorCode, PlainEnglishSummary, StepByStepFix, Upvotes, Downvotes)
        SELECT ?, ?, ?, ?, ?
        WHERE NOT EXISTS (SELECT 1 FROM SOLUTIONS WHERE ErrorCode = ? AND StepByStepFix = ?)
    ''', [(d[0], d[1], d[2], d[3], d[4], d[0], d[2]) for d in initial_solutions_data])

    conn.commit()
    conn.close()
    print(f"Successfully seeded database with {len(initial_solutions_data)} solutions!")
initial_database()

