function results = runExcelModelTests(excelFile, modelName, outputFolder)
% RUNEXCELMODELTESTS Execute Excel-defined tests and save the result table.
%
% Required sheets:
% TestCases: TestID, Description, StopTime
% Inputs: TestID, Variable, Value
% Expected: TestID, Signal, ExpectedFinalValue, AbsTol

    testCases = readtable(excelFile, "Sheet", "TestCases", "TextType", "string");
    inputs = readtable(excelFile, "Sheet", "Inputs", "TextType", "string");
    expected = readtable(excelFile, "Sheet", "Expected", "TextType", "string");

    results = table(strings(height(testCases), 1), strings(height(testCases), 1), ...
        strings(height(testCases), 1), strings(height(testCases), 1), ...
        "VariableNames", {"TestID", "Description", "Status", "Details"});

    for testIndex = 1:height(testCases)
        testID = string(testCases.TestID(testIndex));
        results.TestID(testIndex) = testID;
        results.Description(testIndex) = string(testCases.Description(testIndex));

        try
            simIn = Simulink.SimulationInput(modelName);
            simIn = simIn.setModelParameter("StopTime", string(testCases.StopTime(testIndex)));

            selectedInputs = inputs(string(inputs.TestID) == testID, :);
            for inputIndex = 1:height(selectedInputs)
                value = numericValue(selectedInputs.Value(inputIndex));
                simIn = simIn.setVariable(string(selectedInputs.Variable(inputIndex)), value);
            end

            simOut = sim(simIn);
            selectedExpected = expected(string(expected.TestID) == testID, :);
            failures = strings(0, 1);

            for expectedIndex = 1:height(selectedExpected)
                signalName = string(selectedExpected.Signal(expectedIndex));
                expectedValue = numericValue(selectedExpected.ExpectedFinalValue(expectedIndex));
                tolerance = numericValue(selectedExpected.AbsTol(expectedIndex));

                loggedSignal = simOut.logsout.getElement(char(signalName));
                actualValue = loggedSignal.Values.Data(end);

                if abs(actualValue - expectedValue) > tolerance
                    failures(end + 1) = sprintf("%s: expected %.4f, actual %.4f", ...
                        signalName, expectedValue, actualValue); %#ok<AGROW>
                end
            end

            if isempty(failures)
                results.Status(testIndex) = "PASS";
                results.Details(testIndex) = "All expected outputs matched.";
            else
                results.Status(testIndex) = "FAIL";
                results.Details(testIndex) = strjoin(failures, " | ");
            end
        catch simulationError
            results.Status(testIndex) = "ERROR";
            results.Details(testIndex) = string(simulationError.message);
        end
    end

    writetable(results, fullfile(outputFolder, "TestExecutionReport.xlsx"));
end

function value = numericValue(inputValue)
    if isnumeric(inputValue)
        value = inputValue;
    else
        value = str2double(string(inputValue));
    end

    if isnan(value)
        error("Excel input contains a non-numeric value.");
    end
end
