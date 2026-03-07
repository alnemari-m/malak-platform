"""Standard dataset loaders with recommended transforms."""

import sys
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader

# Windows multiprocessing requires num_workers=0 unless the caller
# wraps everything in if __name__ == '__main__' with freeze_support().
_DEFAULT_WORKERS = 0 if sys.platform == "win32" else 2


CIFAR10_MEAN = (0.4914, 0.4822, 0.4465)
CIFAR10_STD = (0.2023, 0.1994, 0.2010)

FMNIST_MEAN = (0.2860,)
FMNIST_STD = (0.3530,)


def get_cifar10(root="./data", batch_size=128, num_workers=_DEFAULT_WORKERS):
    """Load CIFAR-10 with standard augmentation.

    Returns:
        (train_loader, test_loader, train_dataset, test_dataset)
    """
    transform_train = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(CIFAR10_MEAN, CIFAR10_STD),
    ])

    transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(CIFAR10_MEAN, CIFAR10_STD),
    ])

    train_dataset = torchvision.datasets.CIFAR10(
        root=root, train=True, download=True, transform=transform_train
    )
    test_dataset = torchvision.datasets.CIFAR10(
        root=root, train=False, download=True, transform=transform_test
    )

    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers
    )
    test_loader = DataLoader(
        test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers
    )

    return train_loader, test_loader, train_dataset, test_dataset


def get_fashion_mnist(root="./data", batch_size=128, num_workers=_DEFAULT_WORKERS):
    """Load Fashion-MNIST with standard transforms.

    Returns:
        (train_loader, test_loader, train_dataset, test_dataset)
    """
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(FMNIST_MEAN, FMNIST_STD),
    ])

    train_dataset = torchvision.datasets.FashionMNIST(
        root=root, train=True, download=True, transform=transform
    )
    test_dataset = torchvision.datasets.FashionMNIST(
        root=root, train=False, download=True, transform=transform
    )

    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers
    )
    test_loader = DataLoader(
        test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers
    )

    return train_loader, test_loader, train_dataset, test_dataset
