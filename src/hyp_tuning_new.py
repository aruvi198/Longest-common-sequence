import argparse
import datetime
import time

FINISH_CONDITIONS = ["Succeeded", "Failed"]

def wait_experiment_finish(katib_client, experiment, timeout):
    polling_interval = datetime.timedelta(seconds=30)
    end_time = datetime.datetime.now() + datetime.timedelta(minutes=timeout)
    experiment_name = experiment.metadata.name
    namespace = experiment.metadata.namespace
    print("Exp Name: {} and Namespace {}".format(experiment_name, namespace))
    while True:
        current_status = None
        try:
            time.sleep(60)
            current_status = katib_client.get_experiment_status(name=experiment_name, namespace=namespace)
        except Exception as e:
            if str(e).count("Not Found")>0:
                print("it is not found so conitnuing")
                continue
            else:
                print("some other thing happened : ")
            # print("Unable to get current status for the Experiment: {} in namespace: {}. Exception: {}".format(
            #     experiment_name, namespace, e))
        # If Experiment has reached complete condition, exit the loop.
        if current_status in FINISH_CONDITIONS:
            print("Experiment: {} in namespace: {} has reached the end condition: {}".format(
                experiment_name, namespace, current_status))
            return
        # Print the current condition.
        print("Current condition for Experiment: {} in namespace: {} is: {}".format(
            experiment_name, namespace, current_status))
        # If timeout has been reached, rise an exception.
        if datetime.datetime.now() > end_time:
            print("Inside 1Exeption 1Timeout")

            raise Exception("Timout waiting for Experiment: {} in namespace: {} "
                            "to reach one of these conditions: {}".format(
                                experiment_name, namespace, FINISH_CONDITIONS))
        # Sleep for poll interval.
        print("Sleep at",datetime.datetime.now())
        time.sleep(polling_interval.seconds)
        print("Sleep done",datetime.datetime.now())


def create_dep(mount_path,yaml_path,delete_after_done,timeout,claim_name,output_file):
    print(mount_path,yaml_path,delete_after_done,timeout,claim_name,output_file)
    import os
    import time
    import json
    from kubeflow.katib import KatibClient
    from kubernetes.client import V1ObjectMeta
    from kubeflow.katib import V1beta1Experiment
    from kubeflow.katib import V1beta1AlgorithmSpec
    from kubeflow.katib import V1beta1ObjectiveSpec
    from kubeflow.katib import V1beta1FeasibleSpace
    from kubeflow.katib import V1beta1ExperimentSpec
    from kubeflow.katib import V1beta1ObjectiveSpec
    from kubeflow.katib import V1beta1ParameterSpec
    from kubeflow.katib import V1beta1TrialTemplate
    from kubeflow.katib import V1beta1TrialParameterSpec
    
    #parse yaml to get all the attributes for experiment -- one method
    #or get attributes as arguments for python file -- lots of arguments
    
    #Experiment specifications definition
    
    # Experiment name and namespace.
    namespace = "kubeflow-user-example-com"
    # experiment_name = "katib-game-new2"
    experiment_name = "katib-game"

    #metadata
    metadata = V1ObjectMeta(
        name=experiment_name,
        namespace=namespace
    )

    # Algorithm specification.
    algorithm_spec=V1beta1AlgorithmSpec(
        algorithm_name="random"
    )

    # Objective specification.
    objective_spec=V1beta1ObjectiveSpec(
        type="maximize",
        goal= 0.99,
        # goal= 0.5,
        objective_metric_name="Validation-accuracy",
        additional_metric_names=["Train-accuracy"]
    )

    # Experiment search space. In this example we tune learning rate, number of layer and optimizer.
    parameters=[
        V1beta1ParameterSpec(
            name="lr",
            parameter_type="double",
            feasible_space=V1beta1FeasibleSpace(
                min="0.01",
                max="0.06"
                # max="0.02"
            ),
        ),        
        V1beta1ParameterSpec(
            name="optimizer",
            parameter_type="categorical",
            feasible_space=V1beta1FeasibleSpace(
                list=["sgd", "adam", "ftrl"]
                # list=["sgd"]
            ),
        ),
    ]



    #file to be added to hp tuning component
    # JSON template specification for the Trial's Worker Kubernetes Job.
    trial_spec={
        "apiVersion": "batch/v1",
        "kind": "Job",
        "spec": {
            "template": {
                "metadata": {
                    "annotations": {
                        "sidecar.istio.io/inject": "false"
                    }
                },
                "spec": {
                    "volumes": [
                        {
                        "name": "export-model",
                        "persistentVolumeClaim": {
                            "claimName": "$modelpvc"
                        }
                        }
                    ],
                    "containers": [
                        {
                            "name": "training-container",
                            "image": "docker.io/729578/train:latest",
                            "command": [
                                "python3",
                                "/pipelines/components/train.py",
                                "--data-path=$mount_path",
                                "--batch-size=64",
                                "--loss=crossentropy",
                                "--metrics=accuracy",
                                "--epochs=5",
                                "--learning-rate=${trialParameters.learningRate}",
                                "--optimizer=${trialParameters.optimizer}"
                            ],
                            "volumeMounts": [
                                {
                                "mountPath": "$mount_path",
                                "name": "export-model"
                                }
                            ]
                        }
                    ],
                    "restartPolicy": "Never"
                }
            }
        }
    }
    
    trial_spec["spec"]["template"]["spec"]["volumes"][0]["persistentVolumeClaim"]["claimName"] = claim_name
    trial_spec["spec"]["template"]["spec"]["containers"][0]["volumeMounts"][0]["mountPath"] = mount_path
    # trial_spec["spec"]["template"]["spec"]["containers"][0]["volumeMounts"][0]["name"] = "export-model"
    trial_spec["spec"]["template"]["spec"]["containers"][0]["command"][2] = "--data-path="+mount_path

    print(trial_spec)

    # Configure parameters for the Trial template.
    trial_template=V1beta1TrialTemplate(
        primary_container_name="training-container1",
        trial_parameters=[
            V1beta1TrialParameterSpec(
                name="learningRate",
                description="Learning rate for the training model",
                reference="lr"
            ),
            V1beta1TrialParameterSpec(
                name="optimizer",
                description="Training model optimizer (sdg, adam or ftrl)",
                reference="optimizer"
            ),
        ],
        trial_spec=trial_spec
    )


    # Experiment object.
    experiment = V1beta1Experiment(
        api_version="kubeflow.org/v1beta1",
        kind="Experiment",
        metadata=metadata,
        spec=V1beta1ExperimentSpec(
            max_trial_count=7,
            parallel_trial_count=3,
            max_failed_trial_count=3,
            algorithm=algorithm_spec,
            objective=objective_spec,
            parameters=parameters,
            trial_template=trial_template,
        )
    )

    # Create client.
    katib_client = KatibClient()
    print("creating experiment : ")
    # Create your Experiment.
    output  = katib_client.create_experiment(experiment,namespace=namespace)
    print("created experiment: ")

    print("exp shoulda been created")
    
    #get list of experiments in the namespace
    exp_list = katib_client.get_experiment(namespace=namespace)
    #status = kclient.get_experiment_status(name=experiment_name,namespace=namespace)
    print("experiment list : ")
    
    # Wait until Experiment is created.
    # end_time = datetime.datetime.now() + datetime.timedelta(minutes=15)
    # while True:
    #     current_status = None
    #     # Try to get Experiment status.
    #     try:
    #         current_status = katib_client.get_experiment_status(name=experiment_name, namespace=namespace)
    #     except Exception:
    #         if current_status == "None":
    #             print("Waiting until Experiment is created...")
    #     # If current status is set, exit the loop.
    #     if current_status is not None:
    #         break
    #     # If timeout has been reached, rise an exception.
    #     if datetime.datetime.now() > end_time:
    #         # raise Exception("Timeout waiting for Experiment: {} in namespace: {} to be created".format(
    #         #     experiment_name, namespace))
    #         print("waiting for experiment creation fed up")
    #     time.sleep(1)
                            
    print("Experiment is created")

    # Wait for Experiment finish.
    wait_experiment_finish(katib_client, experiment, timeout)

    # Check if Experiment is successful.
    if katib_client.is_experiment_succeeded(name=experiment_name, namespace=namespace):
        print("Experiment: {} in namespace: {} is successful".format(
            experiment_name, namespace))

        optimal_hp = katib_client.get_optimal_hyperparameters(
            name=experiment_name, namespace=namespace)
        print("Optimal hyperparameters:\n{}".format(optimal_hp))


            
        # Save HyperParameters to the file.
        print(mount_path+output_file)
        with open(mount_path+output_file, 'w') as f:
            f.write(json.dumps(optimal_hp))

        print("output saved")
    else:
        print("Experiment: {} in namespace: {} is failed".format(
            experiment_name, namespace))
        # Print Experiment if it is failed.
        experiment = katib_client.get_experiment(name=experiment_name, namespace=namespace)
        print(experiment)

    # Delete Experiment if it is needed.
    if delete_after_done in ["True","true","TRUE"]:
        print("deleting experiment as goal is achieved")
        katib_client.delete_experiment(name=experiment_name, namespace=namespace)
        print("Experiment: {} in namespace: {} has been deleted".format(
            experiment_name, namespace))
    
    print("over")

#arguments: mount path: path, objective: metrics, parameters in list: [], etc
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="run hyp tuning from container")
    parser.add_argument(
        "--mount-path",
        type=str,
        help="Path of the model structure",
    )
    parser.add_argument(
        "--yaml-path",
        type=str,
        help="Path of the yaml file",
    )
    parser.add_argument(
        "--delete-after-done",
        type=bool,
        help="to delete experiment or not",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        help="experiment timeout in minutes",
    )
    parser.add_argument(
        "--claim-name",
        type=str,
        help="name of pvc claim",
    )
    parser.add_argument(
        "--output-file",
        type=str,        
        default="/output.txt",
        help="output file name to store best hp",
    )
    args, _ = parser.parse_known_args()
    print("mount path args : ",args.mount_path)
    create_dep(args.mount_path,args.yaml_path,args.delete_after_done,args.timeout,args.claim_name,args.output_file)
