from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class Agent:

    def __init__(self, params):
        self.params = params

    def run(self, queue):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get("https://selfdrivingcars.mit.edu/deeptraffic/")

        # change code
        # driver.execute_script('''var editor = document.getElementsByClassName("view-lines")[0];editor.innerText = "''' + self.generate_code(self.params) + '"')
        #editor = driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[2]/div[1]')
        code = self.generate_code(self.params)
        print(code)
        driver.execute_script('editor.setValue("' + code + '")')
        driver.save_screenshot('screenshot1.png')
        # click apply code button
        driver.find_element_by_xpath('//*[@id="main"]/div/div[3]/div[3]/button[1]').click()

        # click train button
        train_button = driver.find_element_by_id("trainButton")
        train_button.click()
        try:
            element = WebDriverWait(driver, 1000).until(
                EC.element_to_be_clickable((By.ID, "trainButton"))
            )
        finally:
            print("training finished")
            # click OK button
            driver.find_element_by_class_name("confirm").click()

        time.sleep(0.1)
        eval_button = driver.find_element_by_xpath('//*[@id="evalButton"]')
        eval_button.click()
        try:
            element = WebDriverWait(driver, 1000).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[7]/div/button"))
            )
        finally:
            print("evaluation finished")
            time.sleep(0.1)
            driver.save_screenshot('screenie.png')
            text_result = driver.find_element_by_xpath("/html/body/div[3]/p/b")
            result_string = text_result.get_attribute('innerHTML')
            print(result_string)
            speed = float(result_string[0:5])

        queue.put(speed)

    @staticmethod
    def generate_code(params):
        print(params)
        code =  'lanesSide = ' + str(params[0]) + ';\\n' + \
                'patchesAhead = ' + str(params[1]) + ';\\n' + \
                'patchesBehind = ' + str(params[2]) + ';\\n' + \
                'trainIterations = ' + str(params[3]) + ';\\n' + \
                'otherAgents = 0;\\n' + \
                'var num_inputs = (lanesSide * 2 + 1) * (patchesAhead + patchesBehind);\\n' + \
                'var num_actions = 5;\\n' + \
                'var temporal_window = 3;\\n' + \
                'var network_size = num_inputs * temporal_window + num_actions * temporal_window + num_inputs;\\n' + \
                'var layer_defs = [];\\n' + \
                '    layer_defs.push({\\n' + \
                '    type: "input",\\n' + \
                '    out_sx: 1,\\n' + \
                '    out_sy: 1,\\n' + \
                '    out_depth: network_size\\n' + \
                ' });\\n' + \
                'layer_defs.push({\\n' + \
                '    type: "fc",\\n' + \
                '    num_neurons = ' + str(params[4]) + ',\\n' + \
                '    activation: "relu"\\n' + \
                '});\\n' + \
                'layer_defs.push({\\n' + \
                '    type: "fc",\\n' + \
                '    num_neurons = ' + str(params[5]) + ',\\n' + \
                '    activation: "relu"\\n' + \
                '});\\n' + \
                'layer_defs.push({\\n' + \
                '    type: "fc",\\n' + \
                '    num_neurons = ' + str(params[6]) + ',\\n' + \
                '    activation: "relu"\\n' + \
                '});\\n' + \
                'layer_defs.push({\\n' + \
                '    type: "regression",\\n' + \
                '    num_neurons: num_actions\\n' + \
                '});\\n' + \
                'var tdtrainer_options = {\\n' + \
                '    learning_rate: 0.001,\\n' + \
                '    momentum: 0.0,\\n' + \
                '    batch_size: 64,\\n' + \
                '    l2_decay: 0.01\\n' + \
                '};\\n' + \
                'var opt = {};\\n' + \
                '    opt.temporal_window = temporal_window;\\n' + \
                '    opt.experience_size = 3000;\\n' + \
                '    opt.start_learn_threshold = 500;\\n' + \
                '    opt.gamma = 0.88;\\n' + \
                '    opt.learning_steps_total = 10000;\\n' + \
                '    opt.learning_steps_burnin = 1000;\\n' + \
                '    opt.epsilon_min = 0.0;\\n' + \
                '    opt.epsilon_test_time = 0.0;\\n' + \
                '    opt.layer_defs = layer_defs;\\n' + \
                '    opt.tdtrainer_options = tdtrainer_options;\\n' + \
                '    brain = new deepqlearn.Brain(num_inputs, num_actions, opt);\\n' + \
                '    learn = function (state, lastReward) {\\n' + \
                '        brain.backward(lastReward);\\n' + \
                '        var action = brain.forward(state);\\n' + \
                '        draw_net();\\n' + \
                '        draw_stats();\\n' + \
                '        return action;\\n' + \
                '        return action;\\n' + \
                '        }\\n' + \
                '//]]>'

        return code