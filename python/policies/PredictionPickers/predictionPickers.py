import numpy as np

class PredictionPickers:
    @staticmethod
    def pickMax(result):
        maxIndex = np.argmax(result)
        return maxIndex

    @staticmethod
    def eGreedyPicker(result, epsilon):
        random = np.random.random()
        if random < epsilon:
            return np.random.randint(0, result.shape[1])
        else:
            return PredictionPickers.pickMax(result)    

    @staticmethod
    def upByMin(self, probs):
        lowest = probs[0]
        for i in range(1, len(probs)):
            if probs[i][0] < lowest:
                lowest = probs[i][0]
        # sm = probs.map(n => [n[0] + (-lowest)])
        sm = [n[0] + (-lowest) for n in probs]
        return sm    

    @staticmethod
    def pickIndexOverDistribution(result):
        sm = PredictionPickers.upByMin(result.numpy())
        sum = 0
        for n in sm:
            sum += np.power(n, 3)
        resultDistribution = [np.power(n, 3) / sum for n in sm]
        random = np.random.random()
        threshold = 0
        for i in range(0, len(resultDistribution)):
            threshold += resultDistribution[i]
            if random < threshold:
                return i
        return len(resultDistribution) - 1

    @staticmethod
    def pickOverSoftmax(self, result):
        # exps = result.numpy().map(n => np.exp(n))
        exps = [np.exp(n) for n in result.numpy()]
        sum = 0
        for n in exps:
            sum += n
        # probs = exps.map(n => n / sum)
        probs = [n / sum for n in exps]
        random = np.random.random()
        threshold = 0
        for i in range(0, len(probs)):
            threshold += probs[i]
            if random < threshold:
                return i
        return len(probs) - 1