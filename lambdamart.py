import pyltr

if __name__ == '__main__':
    #folder = '/Users/mohit/Documents/Grad_Courses/spring20/info-retrieval/learning_to_rank/MQ2008/Fold1/'
    folder = '/Users/wery/Desktop/BAJiawenWang/dataset/MQ2008/Fold1/'

    with open(folder + 'train.txt') as trainfile, \
            open(folder + 'vali.txt') as valifile, \
            open(folder + 'test.txt') as evalfile:
        TX, Ty, Tqids, _ = pyltr.data.letor.read_dataset(trainfile)
        VX, Vy, Vqids, _ = pyltr.data.letor.read_dataset(valifile)
        EX, Ey, Eqids, _ = pyltr.data.letor.read_dataset(evalfile)

        metric = pyltr.metrics.NDCG(k=10)

        # Only needed if you want to perform validation (early stopping & trimming)
        # monitor = pyltr.models.monitors.ValidationMonitor(
        #     VX, Vy, Vqids, metric=metric, stop_after=10)

        model = pyltr.models.LambdaMART(
            metric=metric,
            n_estimators=20,
            learning_rate=0.02,
            max_features=0.5,
            query_subsample=0.5,
            max_leaf_nodes=10,
            min_samples_leaf=64,
            verbose=1,
        )

        #model.fit(TX, Ty, Tqids, monitor=monitor)
        model.fit(TX, Ty, Tqids)

        Epred = model.predict(EX)
        print('Random ranking:', metric.calc_mean_random(Eqids, Ey))
        print('Our model:', metric.calc_mean(Eqids, Ey, Epred))