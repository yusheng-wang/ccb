"""Machine learning utility functions"""
import multiprocessing as _mp

from sklearn import ensemble as _ensemble
from sklearn import linear_model as _linear_model
from sklearn import metrics as _metrics
from sklearn import model_selection as _model_selection
from sklearn import svm as _svm
from sklearn import tree as _tree

# global runtime settings
_ncpu = _mp.cpu_count()


class tuner(object):
    def __init__(
        self,
        x,
        y,
        optimizer=_model_selection.GridSearchCV,
        param_grid=None,
        scoring=None,
        fit_params=None,
        n_jobs=_ncpu,
        refit=True,
        verbose=1,
        error_score="raise",
        return_train_score=True,
        cv=None,
        n_splits=5,
    ):
        """Initializes a model tuning object wtih functions to optimize hyperparameter selection across multiple sklearn model types
        :param x: the model covariates
        :param y: the response variable
        :param optimizer: the parameter search and optimization method. default is a sklearn.model_selection.GridSearchCV instance
        :param param_grid: dictionary with hyperparameter names as keys and lists of hyperparameter settings to try in grid search
        :param scoring: the model performance metric to optimize. accepts string values and sklear.metrics.* instances
        :param fit_params: parameters to pass to the `fit` method of the estimator
        :param n_jobs: number of cpus to use in parameter estimation
        :param refit: compute and store a `best_estimator_` based on the best hyperparameter fit
        :param error_score: the value to return whenan error occurs in fitting. set to 'raise' to raise an exception.
        :param return_train_score: boolean to compute and save training scores. setting to false may save computation time.
        :param cv: determines the cross-validation splitting strategy. accepts inputs to sklearn.model_selection.GridSearchCV
        :param n_splits: number of cross-validation splits
        :return object: a class instance with model tuning utilities / functions
        """

        # set the variables to the tune class
        self.x = x
        self.y = y
        self.optimizer = optimizer
        self.param_grid = param_grid
        self.scoring = scoring
        self.fit_params = fit_params
        self.n_jobs = n_jobs
        self.refit = refit
        self.verbose = verbose
        self.error_score = error_score
        self.return_train_score = return_train_score
        self.cv = cv
        self.n_splits = n_splits

    def run_gs(self, estimator):
        """Runs a grid search based on the input hyperparameter options.
        :param estimator: the sklearn model estimator with an estimator.fit() function
        :return None: updates the tuner object with grid search results
        """

        # create the grid search
        gs = self.optimizer(
            estimator,
            param_grid=self.param_grid,
            scoring=self.scoring,
            n_jobs=self.n_jobs,
            cv=self.cv,
            refit=self.refit,
            verbose=self.verbose,
            error_score=self.error_score,
            return_train_score=self.return_train_score,
        )

        # begin fitting the grid search
        gs.fit(self.x, self.y)

        # update the tuning object with the outputs of the tuning
        self.cv_results = gs.cv_results_
        self.best_estimator = gs.best_estimator_
        self.best_score = gs.best_score_
        self.best_params = gs.best_params_
        self.best_index = gs.best_index_
        self.scorer = gs.scorer_
        self.n_splits = gs.n_splits_
        self.gs = gs

    def LinearRegression(self, optimizer=None, param_grid=None, scoring=None, fit_params=None, cv=None):
        """Creates a linear regression model estimator.
        :param optimizer: the parameter search and optimization method. default is a sklearn.model_selection.GridSearchCV instance
        :param param_grid: dictionary with hyperparameter names as keys and lists of hyperparameter settings to try in grid search
        :param scoring: the model performance metric to optimize. accepts string values and sklear.metrics.* instances
        :param fit_params: parameters to pass to the `fit` method of the estimator
        :param cv: determines the cross-validation splitting strategy. accepts inputs to sklearn.model_selection.GridSearchCV
        :return None: updates the `tuner` object with the passed parameters and runs a grid search using the LinearRegression estimator
        """

        # check if the optimizer has changed, otherwise use default
        if optimizer is not None:
            self.optimizer = optimizer

        # check if the parameter grid has been set, otherwise set defaults
        if param_grid is None:
            if self.param_grid is None:
                param_grid = {"normalize": (True, False), "fit_intercept": (True, False)}
                self.param_grid = param_grid
        else:
            self.param_grid = param_grid

        # set the scoring function
        if scoring is None:
            if self.scoring is None:
                scoring = _metrics.explained_variance_score
                self.scoring = scoring
        else:
            self.scoring = scoring

        # set the default fit parameters
        if fit_params is not None:
            self.fit_params = fit_params

        # set the cross validation strategy
        if cv is None:
            if self.cv is None:
                cv = _model_selection.StratifiedKFold(n_splits=self.n_splits)
                self.cv = cv
        else:
            self.cv = cv

        # create the estimator and run the grid search
        estimator = _linear_model.LinearRegression()
        self.run_gs(estimator)

    def LogisticRegression(self, optimizer=None, param_grid=None, scoring=None, fit_params=None, cv=None):
        """Creates a logistic regression model estimator.
        :param optimizer: the parameter search and optimization method. default is a sklearn.model_selection.GridSearchCV instance
        :param param_grid: dictionary with hyperparameter names as keys and lists of hyperparameter settings to try in grid search
        :param scoring: the model performance metric to optimize. accepts string values and sklear.metrics.* instances
        :param fit_params: parameters to pass to the `fit` method of the estimator
        :param cv: determines the cross-validation splitting strategy. accepts inputs to sklearn.model_selection.GridSearchCV
        :return None: updates the `tuner` object with the passed parameters and runs a grid search using the LogisticRegression estimator
        """

        # check if the optimizer has changed, otherwise use default
        if optimizer is not None:
            self.optimizer = optimizer

        # check if the parameter grid has been set, otherwise set defaults
        if param_grid is None:
            if self.param_grid is None:
                param_grid = {"C": (1e-2, 1e-1, 1e0, 1e1), "tol": (1e-3, 1e-4, 1e-5), "fit_intercept": (True, False)}
                self.param_grid = param_grid
        else:
            self.param_grid = param_grid

        # set the scoring function
        if scoring is None:
            if self.scoring is None:
                scoring = "roc_auc"
                self.scoring = scoring
        else:
            self.scoring = scoring

        # set the default fit parameters
        if fit_params is not None:
            self.fit_params = fit_params

        # set the cross validation strategy
        if cv is None:
            if self.cv is None:
                cv = _model_selection.StratifiedKFold(n_splits=self.n_splits)
                self.cv = cv
        else:
            self.cv = cv

        # create the estimator and run the grid search
        estimator = _linear_model.LogisticRegression()
        self.run_gs(estimator)

    def DecisionTreeClassifier(self, optimizer=None, param_grid=None, scoring=None, fit_params=None, cv=None):
        """Creates a decision tree model estimator.
        :param optimizer: the parameter search and optimization method. default is a sklearn.model_selection.GridSearchCV instance
        :param param_grid: dictionary with hyperparameter names as keys and lists of hyperparameter settings to try in grid search
        :param scoring: the model performance metric to optimize. accepts string values and sklear.metrics.* instances
        :param fit_params: parameters to pass to the `fit` method of the estimator
        :param cv: determines the cross-validation splitting strategy. accepts inputs to sklearn.model_selection.GridSearchCV
        :return None: updates the `tuner` object with the passed parameters and runs a grid search using the DecisionTreeClassifier estimator
        """

        # check if the optimizer has changed, otherwise use default
        if optimizer is not None:
            self.optimizer = optimizer

        # check if the parameter grid has been set, otherwise set defaults
        if param_grid is None:
            if self.param_grid is None:
                param_grid = {
                    "criterion": ("gini", "entropy"),
                    "splitter": ("best", "random"),
                    "max_features": ("sqrt", "log2", None),
                    "max_depth": (2, 5, 10, None),
                    "min_samples_split": (2, 0.01, 0.1),
                    "min_impurity_split": (1e-7, 1e-6),
                }
                self.param_grid = param_grid
        else:
            self.param_grid = param_grid

        # set the scoring function
        if scoring is None:
            if self.scoring is None:
                scoring = "neg_log_loss"
                self.scoring = scoring
        else:
            self.scoring = scoring

        # set the default fit parameters
        if fit_params is not None:
            self.fit_params = fit_params

        # set the cross validation strategy
        if cv is None:
            if self.cv is None:
                cv = _model_selection.StratifiedKFold(n_splits=self.n_splits)
                self.cv = cv
        else:
            self.cv = cv

        # create the estimator and run the grid search
        estimator = _tree.DecisionTreeClassifier()
        self.run_gs(estimator)

    def SVC(self, optimizer=None, param_grid=None, scoring=None, fit_params=None, cv=None, class_weight=None):
        """Creates a support vector machine classifier model estimator.
        :param optimizer: the parameter search and optimization method. default is a sklearn.model_selection.GridSearchCV instance
        :param param_grid: dictionary with hyperparameter names as keys and lists of hyperparameter settings to try in grid search
        :param scoring: the model performance metric to optimize. accepts string values and sklear.metrics.* instances
        :param fit_params: parameters to pass to the `fit` method of the estimator
        :param cv: determines the cross-validation splitting strategy. accepts inputs to sklearn.model_selection.GridSearchCV
        :return None: updates the `tuner` object with the passed parameters and runs a grid search using the SVC estimator
        """

        # check if the optimizer has changed, otherwise use default
        if optimizer is not None:
            self.optimizer = optimizer

        # check if the parameter grid has been set, otherwise set defaults
        if param_grid is None:
            if self.param_grid is None:
                param_grid = {
                    "C": (1e-3, 1e-2, 1e-1, 1e0, 1e1),
                    "kernel": ("rbf", "linear"),
                    "gamma": (1e-3, 1e-4, 1e-5, 1e-6, 1e-7),
                }
        self.param_grid = param_grid

        # set the scoring function
        if scoring is None:
            if self.scoring is None:
                scoring = "neg_log_loss"
        self.scoring = scoring

        # set the default fit parameters
        if fit_params is not None:
            self.fit_params = fit_params

        # set the cross validation strategy
        if cv is None:
            if self.cv is None:
                cv = _model_selection.StratifiedKFold(n_splits=self.n_splits)
        self.cv = cv

        # set the class weight
        if class_weight is not None:
            if self.class_weight is None:
                class_weight = "balanced"
        self.param_grid["class_weight"] = class_weight

        # create the estimator and run the grid search
        estimator = _svm.SVC()
        self.run_gs(estimator)

    def SVR(self, optimizer=None, param_grid=None, scoring=None, fit_params=None, cv=None):
        """Creates a support vector machine regression model estimator.
        :param optimizer: the parameter search and optimization method. default is a sklearn.model_selection.GridSearchCV instance
        :param param_grid: dictionary with hyperparameter names as keys and lists of hyperparameter settings to try in grid search
        :param scoring: the model performance metric to optimize. accepts string values and sklear.metrics.* instances
        :param fit_params: parameters to pass to the `fit` method of the estimator
        :param cv: determines the cross-validation splitting strategy. accepts inputs to sklearn.model_selection.GridSearchCV
        :return None: updates the `tuner` object with the passed parameters and runs a grid search using the SVR estimator
        """

        # check if the optimizer has changed, otherwise use default
        if optimizer is not None:
            self.optimizer = optimizer

        # check if the parameter grid has been set, otherwise set defaults
        if param_grid is None:
            if self.param_grid is None:
                param_grid = {
                    "C": (1e-2, 1e-1, 1e0, 1e1),
                    "epsilon": (0.01, 0.1, 1),
                    "kernel": ("rbf", "linear", "poly", "sigmoid"),
                    "gamma": (1e-2, 1e-3, 1e-4),
                }
                self.param_grid = param_grid
        else:
            self.param_grid = param_grid

        # set the scoring function
        if scoring is None:
            if self.scoring is None:
                scoring = _metrics.explained_variance_score
                self.scoring = scoring
        else:
            self.scoring = scoring

        # set the default fit parameters
        if fit_params is not None:
            self.fit_params = fit_params

        # set the cross validation strategy
        if cv is None:
            if self.cv is None:
                cv = _model_selection.StratifiedKFold(n_splits=self.n_splits)
                self.cv = cv
        else:
            self.cv = cv

        # create the estimator and run the grid search
        estimator = _svm.SVR()
        self.run_gs(estimator)

    def LinearSVC(self, optimizer=None, param_grid=None, scoring=None, fit_params=None, cv=None):
        """Creates a linear support vector machine classifaction model estimator.
        :param optimizer: the parameter search and optimization method. default is a sklearn.model_selection.GridSearchCV instance
        :param param_grid: dictionary with hyperparameter names as keys and lists of hyperparameter settings to try in grid search
        :param scoring: the model performance metric to optimize. accepts string values and sklear.metrics.* instances
        :param fit_params: parameters to pass to the `fit` method of the estimator
        :param cv: determines the cross-validation splitting strategy. accepts inputs to sklearn.model_selection.GridSearchCV
        :return None: updates the `tuner` object with the passed parameters and runs a grid search using the LinearSVC estimator
        """

        # check if the optimizer has changed, otherwise use default
        if optimizer is not None:
            self.optimizer = optimizer

        # check if the parameter grid has been set, otherwise set defaults
        if param_grid is None:
            if self.param_grid is None:
                param_grid = {
                    "C": (1e-2, 1e-1, 1e0, 1e1),
                    "loss": ("hinge", "squared_hinge"),
                    "tol": (1e-3, 1e-4, 1e-5),
                    "fit_intercept": (True, False),
                }
                self.param_grid = param_grid
        else:
            self.param_grid = param_grid

        # set the scoring function
        if scoring is None:
            if self.scoring is None:
                scoring = "neg_log_loss"
                self.scoring = scoring
        else:
            self.scoring = scoring

        # set the default fit parameters
        if fit_params is not None:
            self.fit_params = fit_params

        # set the cross validation strategy
        if cv is None:
            if self.cv is None:
                cv = _model_selection.StratifiedKFold(n_splits=self.n_splits)
                self.cv = cv
        else:
            self.cv = cv

        # create the estimator and run the grid search
        estimator = _svm.LinearSVC()
        self.run_gs(estimator)

    def LinearSVR(self, optimizer=None, param_grid=None, scoring=None, fit_params=None, cv=None):
        """Creates a linear support vector machine regression model estimator.
        :param optimizer: the parameter search and optimization method. default is a sklearn.model_selection.GridSearchCV instance
        :param param_grid: dictionary with hyperparameter names as keys and lists of hyperparameter settings to try in grid search
        :param scoring: the model performance metric to optimize. accepts string values and sklear.metrics.* instances
        :param fit_params: parameters to pass to the `fit` method of the estimator
        :param cv: determines the cross-validation splitting strategy. accepts inputs to sklearn.model_selection.GridSearchCV
        :return None: updates the `tuner` object with the passed parameters and runs a grid search using the LinearSVR estimator
        """

        # check if the optimizer has changed, otherwise use default
        if optimizer is not None:
            self.optimizer = optimizer

        # check if the parameter grid has been set, otherwise set defaults
        if param_grid is None:
            if self.param_grid is None:
                param_grid = {
                    "C": (1e-2, 1e-1, 1e0, 1e1),
                    "loss": ("epsilon_insensitive", "squared_epsilon_insensitive"),
                    "epsilon": (0, 0.01, 0.1),
                    "dual": (False),
                    "tol": (1e-3, 1e-4, 1e-5),
                    "fit_intercept": (True, False),
                }
                self.param_grid = param_grid
        else:
            self.param_grid = param_grid

        # set the scoring function
        if scoring is None:
            if self.scoring is None:
                scoring = _metrics.explained_variance_score
                self.scoring = scoring
        else:
            self.scoring = scoring

        # set the default fit parameters
        if fit_params is not None:
            self.fit_params = fit_params

        # set the cross validation strategy
        if cv is None:
            if self.cv is None:
                cv = _model_selection.StratifiedKFold(n_splits=self.n_splits)
                self.cv = cv
        else:
            self.cv = cv

        # create the estimator and run the grid search
        estimator = _svm.LinearSVR()
        self.run_gs(estimator)

    def AdaBoostClassifier(self, optimizer=None, param_grid=None, scoring=None, fit_params=None, cv=None):
        """Creates an ADA boosted classifaction model estimator.
        :param optimizer: the parameter search and optimization method. default is a sklearn.model_selection.GridSearchCV instance
        :param param_grid: dictionary with hyperparameter names as keys and lists of hyperparameter settings to try in grid search
        :param scoring: the model performance metric to optimize. accepts string values and sklear.metrics.* instances
        :param fit_params: parameters to pass to the `fit` method of the estimator
        :param cv: determines the cross-validation splitting strategy. accepts inputs to sklearn.model_selection.GridSearchCV
        :return None: updates the `tuner` object with the passed parameters and runs a grid search using the AdaBoostClassifier estimator
        """

        # check if the optimizer has changed, otherwise use default
        if optimizer is not None:
            self.optimizer = optimizer

        # check if the parameter grid has been set, otherwise set defaults
        if param_grid is None:
            if self.param_grid is None:
                param_grid = {"n_estimators": (25, 50, 75, 100), "learning_rate": (0.1, 0.5, 1.0)}
                self.param_grid = param_grid
        else:
            self.param_grid = param_grid

        # set the scoring function
        if scoring is None:
            if self.scoring is None:
                scoring = "neg_log_loss"
                self.scoring = scoring
        else:
            self.scoring = scoring

        # set the default fit parameters
        if fit_params is not None:
            self.fit_params = fit_params

        # set the cross validation strategy
        if cv is None:
            if self.cv is None:
                cv = _model_selection.StratifiedKFold(n_splits=self.n_splits)
                self.cv = cv
        else:
            self.cv = cv

        # create the estimator and run the grid search
        estimator = _ensemble.AdaBoostClassifier()
        self.run_gs(estimator)

    def AdaBoostRegressor(self, optimizer=None, param_grid=None, scoring=None, fit_params=None, cv=None):
        """Creates an ADA boosted regression model estimator.
        :param optimizer: the parameter search and optimization method. default is a sklearn.model_selection.GridSearchCV instance
        :param param_grid: dictionary with hyperparameter names as keys and lists of hyperparameter settings to try in grid search
        :param scoring: the model performance metric to optimize. accepts string values and sklear.metrics.* instances
        :param fit_params: parameters to pass to the `fit` method of the estimator
        :param cv: determines the cross-validation splitting strategy. accepts inputs to sklearn.model_selection.GridSearchCV
        :return None: updates the `tuner` object with the passed parameters and runs a grid search using the AdaBoostRegressor estimator
        """

        # check if the optimizer has changed, otherwise use default
        if optimizer is not None:
            self.optimizer = optimizer

        # check if the parameter grid has been set, otherwise set defaults
        if param_grid is None:
            if self.param_grid is None:
                param_grid = {
                    "n_estimators": (25, 50, 75, 100),
                    "learning_rate": (0.1, 0.5, 1.0),
                    "loss": ("linear", "exponential", "square"),
                }
                self.param_grid = param_grid
        else:
            self.param_grid = param_grid

        # set the scoring function
        if scoring is None:
            if self.scoring is None:
                scoring = _metrics.explained_variance_score
                self.scoring = scoring
        else:
            self.scoring = scoring

        # set the default fit parameters
        if fit_params is not None:
            self.fit_params = fit_params

        # set the cross validation strategy
        if cv is None:
            if self.cv is None:
                cv = _model_selection.StratifiedKFold(n_splits=self.n_splits)
                self.cv = cv
        else:
            self.cv = cv

        # create the estimator and run the grid search
        estimator = _ensemble.AdaBoostRegressor()
        self.run_gs(estimator)

    def GradientBoostClassifier(self, optimizer=None, param_grid=None, scoring=None, fit_params=None, cv=None):
        """Creates an gradient boosted classifaction model estimator.
        :param optimizer: the parameter search and optimization method. default is a sklearn.model_selection.GridSearchCV instance
        :param param_grid: dictionary with hyperparameter names as keys and lists of hyperparameter settings to try in grid search
        :param scoring: the model performance metric to optimize. accepts string values and sklear.metrics.* instances
        :param fit_params: parameters to pass to the `fit` method of the estimator
        :param cv: determines the cross-validation splitting strategy. accepts inputs to sklearn.model_selection.GridSearchCV
        :return None: updates the `tuner` object with the passed parameters and runs a grid search using the GradientBoostClassifier estimator
        """

        # check if the optimizer has changed, otherwise use default
        if optimizer is not None:
            self.optimizer = optimizer

        # check if the parameter grid has been set, otherwise set defaults
        if param_grid is None:
            if self.param_grid is None:
                param_grid = {
                    "n_estimators": (10, 100, 500),
                    "learning_rate": (0.01, 0.1, 0.5),
                    "max_features": ("sqrt", "log2", None),
                    "max_depth": (1, 10, None),
                    "min_samples_split": (2, 0.01, 0.1),
                }
                self.param_grid = param_grid
        else:
            self.param_grid = param_grid

        # set the scoring function
        if scoring is None:
            if self.scoring is None:
                scoring = "neg_log_loss"
                self.scoring = scoring
        else:
            self.scoring = scoring

        # set the default fit parameters
        if fit_params is not None:
            self.fit_params = fit_params

        # set the cross validation strategy
        if cv is None:
            if self.cv is None:
                cv = _model_selection.StratifiedKFold(n_splits=self.n_splits)
                self.cv = cv
        else:
            self.cv = cv

        # create the estimator and run the grid search
        estimator = _ensemble.GradientBoostingClassifier()
        self.run_gs(estimator)

    def GradientBoostRegressor(self, optimizer=None, param_grid=None, scoring=None, fit_params=None, cv=None):
        """Creates an gradient boosted regression model estimator.
        :param optimizer: the parameter search and optimization method. default is a sklearn.model_selection.GridSearchCV instance
        :param param_grid: dictionary with hyperparameter names as keys and lists of hyperparameter settings to try in grid search
        :param scoring: the model performance metric to optimize. accepts string values and sklear.metrics.* instances
        :param fit_params: parameters to pass to the `fit` method of the estimator
        :param cv: determines the cross-validation splitting strategy. accepts inputs to sklearn.model_selection.GridSearchCV
        :return None: updates the `tuner` object with the passed parameters and runs a grid search using the GradientBoostRegressor estimator
        """

        # check if the optimizer has changed, otherwise use default
        if optimizer is not None:
            self.optimizer = optimizer

        # check if the parameter grid has been set, otherwise set defaults
        if param_grid is None:
            if self.param_grid is None:
                param_grid = {
                    "n_estimators": (10, 100, 500),
                    "learning_rate": (0.01, 0.1, 0.5),
                    "max_features": ("sqrt", "log2", None),
                    "max_depth": (1, 10, None),
                    "min_samples_split": (2, 0.01, 0.1),
                }
                self.param_grid = param_grid
        else:
            self.param_grid = param_grid

        # set the scoring function
        if scoring is None:
            if self.scoring is None:
                scoring = "neg_mean_absolute_error"
                self.scoring = scoring
        else:
            self.scoring = scoring

        # set the default fit parameters
        if fit_params is not None:
            self.fit_params = fit_params

        # set the cross validation strategy
        if cv is None:
            if self.cv is None:
                cv = _model_selection.KFold(n_splits=self.n_splits)
                self.cv = cv
        else:
            self.cv = cv

        # create the estimator and run the grid search
        estimator = _ensemble.GradientBoostingRegressor()
        self.run_gs(estimator)

    def RandomForestClassifier(
        self, optimizer=None, param_grid=None, scoring=None, fit_params=None, cv=None, class_weight=None
    ):
        """Creates a random forest classification model estimator.
        :param optimizer: the parameter search and optimization method. default is a sklearn.model_selection.GridSearchCV instance
        :param param_grid: dictionary with hyperparameter names as keys and lists of hyperparameter settings to try in grid search
        :param scoring: the model performance metric to optimize. accepts string values and sklear.metrics.* instances
        :param fit_params: parameters to pass to the `fit` method of the estimator
        :param cv: determines the cross-validation splitting strategy. accepts inputs to sklearn.model_selection.GridSearchCV
        :param class_weight: per-class weighting factors
        :return None: updates the `tuner` object with the passed parameters and runs a grid search using the RandomForestClassifier estimator
        """

        # check if the optimizer has changed, otherwise use default
        if optimizer is not None:
            self.optimizer = optimizer

        # check if the parameter grid has been set, otherwise set defaults
        if param_grid is None:
            if self.param_grid is None:
                param_grid = {
                    "criterion": ("gini", "entropy"),
                    "n_estimators": (10, 100, 500),
                    "max_features": ("sqrt", "log2", None),
                    "max_depth": (1, 10, None),
                    "min_samples_split": (2, 0.01, 0.1),
                }
                self.param_grid = param_grid
        else:
            self.param_grid = param_grid

        # set the scoring function
        if scoring is None:
            if self.scoring is None:
                scoring = "neg_log_loss"
                self.scoring = scoring
        else:
            self.scoring = scoring

        # set the default fit parameters
        if fit_params is not None:
            self.fit_params = fit_params

        # set the cross validation strategy
        if cv is None:
            if self.cv is None:
                cv = _model_selection.StratifiedKFold(n_splits=self.n_splits)
                self.cv = cv
        else:
            self.cv = cv

        # create the estimator and run the grid search
        estimator = _ensemble.RandomForestClassifier(class_weight=class_weight)
        self.run_gs(estimator)

    def RandomForestRegressor(self, optimizer=None, param_grid=None, scoring=None, fit_params=None, cv=None):
        """Creates a random forest regression model estimator.
        :param optimizer: the parameter search and optimization method. default is a sklearn.model_selection.GridSearchCV instance
        :param param_grid: dictionary with hyperparameter names as keys and lists of hyperparameter settings to try in grid search
        :param scoring: the model performance metric to optimize. accepts string values and sklear.metrics.* instances
        :param fit_params: parameters to pass to the `fit` method of the estimator
        :param cv: determines the cross-validation splitting strategy. accepts inputs to sklearn.model_selection.GridSearchCV
        :return None: updates the `tuner` object with the passed parameters and runs a grid search using the RandomForestRegressor estimator
        """

        # check if the optimizer has changed, otherwise use default
        if optimizer is not None:
            self.optimizer = optimizer

        # check if the parameter grid has been set, otherwise set defaults
        if param_grid is None:
            if self.param_grid is None:
                param_grid = {
                    "n_estimators": (10, 100, 500),
                    "max_features": ("sqrt", "log2", None),
                    "max_depth": (1, 10, None),
                    "min_samples_split": (2, 0.01, 0.1),
                }
                self.param_grid = param_grid
        else:
            self.param_grid = param_grid

        # set the scoring function
        if scoring is None:
            if self.scoring is None:
                scoring = "neg_mean_absolute_error"
                self.scoring = scoring
        else:
            self.scoring = scoring

        # set the default fit parameters
        if fit_params is not None:
            self.fit_params = fit_params

        # set the cross validation strategy
        if cv is None:
            if self.cv is None:
                cv = _model_selection.KFold(n_splits=self.n_splits)
                self.cv = cv
        else:
            self.cv = cv

        # create the estimator and run the grid search
        estimator = _ensemble.RandomForestRegressor()
        self.run_gs(estimator)
