
import pytorch_lightning as pl
import torch
from torch.utils.data.dataloader import DataLoader
import torch.multiprocessing as mp 
from torch.utils.data.sampler import WeightedRandomSampler, RandomSampler



class DataModule(pl.LightningDataModule):

    def __init__(self,
                 ds_train: object=None,
                 ds_val:object =None,
                 ds_test:object =None,
                 batch_size: int = 1,
                 batch_size_val:int = None,
                 batch_size_test:int = None,
                 num_train_samples:int = None,
                 num_workers: int = mp.cpu_count(),
                 seed: int = 0, 
                 pin_memory: bool = False,
                 weights: list = None 
                ):
        super().__init__()
        self.hyperparameters = {**locals()}
        self.hyperparameters.pop('__class__')
        self.hyperparameters.pop('self')

        self.ds_train = ds_train 
        self.ds_val = ds_val 
        self.ds_test = ds_test 

        self.batch_size = batch_size
        self.batch_size_val = batch_size if batch_size_val is None else batch_size_val 
        self.batch_size_test = batch_size if batch_size_test is None else batch_size_test 
        self.num_train_samples = num_train_samples
        self.num_workers = num_workers
        self.seed = seed 
        self.pin_memory = pin_memory
        self.weights = weights

   

    def train_dataloader(self):
        generator = torch.Generator()
        generator.manual_seed(self.seed)
        
        if self.ds_train is not None:
            if self.weights is not None:
                num_samples = len(self.weights) if self.num_train_samples is None else self.num_train_samples
                sampler = WeightedRandomSampler(self.weights, num_samples=num_samples, generator=generator) 
            else:
                num_samples = len(self.ds_train) if self.num_train_samples is None else self.num_train_samples
                sampler = RandomSampler(self.ds_train, num_samples=num_samples, replacement=False, generator=generator)
            return DataLoader(self.ds_train, batch_size=self.batch_size, num_workers=self.num_workers, 
                            sampler=sampler, generator=generator, drop_last=True, pin_memory=self.pin_memory)
        
        raise AssertionError("A training set was not initialized.")

    def val_dataloader(self):
        generator = torch.Generator()
        generator.manual_seed(self.seed)
        if self.ds_val is not None:
            return DataLoader(self.ds_val, batch_size=self.batch_size_val, num_workers=self.num_workers, shuffle=False, 
                                generator=generator, drop_last=False, pin_memory=self.pin_memory)
        
        raise AssertionError("A validation set was not initialized.")


    def test_dataloader(self):
        generator = torch.Generator()
        generator.manual_seed(self.seed)
        if self.ds_test is not None:
            return DataLoader(self.ds_test, batch_size=self.batch_size_test, num_workers=self.num_workers, shuffle=False, 
                            generator = generator, drop_last=False, pin_memory=self.pin_memory)
       
        raise AssertionError("A test test set was not initialized.")

   