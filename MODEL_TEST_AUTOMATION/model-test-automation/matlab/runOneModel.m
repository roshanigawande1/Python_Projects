function runOneModel(testExcelFile, modelFile, reportFolder, createCoverage)
% RUNONEMODEL Run Excel tests for one Simulink model, then create reports.

    if nargin < 4
        createCoverage = false;
    end

    [modelFolder, modelName] = fileparts(modelFile);
    addpath(modelFolder);
    load_system(modelFile);
    cleanupObject = onCleanup(@() close_system(modelName, 0)); %#ok<NASGU>

    if ~isfolder(reportFolder)
        mkdir(reportFolder);
    end

    runExcelModelTests(testExcelFile, modelName, reportFolder);

    if createCoverage
        try
            coverageTest = cvtest(modelName);
            coverageTest.settings.decision = 1;
            coverageTest.settings.condition = 1;
            coverageData = cvsim(coverageTest);
            cvhtml(fullfile(reportFolder, "ModelCoverageReport.html"), coverageData);
        catch coverageError
            warning("Coverage report was not created: %s", coverageError.message);
        end
    end
end
