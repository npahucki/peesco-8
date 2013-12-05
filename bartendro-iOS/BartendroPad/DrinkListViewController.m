//
//  ViewController.m
//  BartendroPad
//
//  Created by Pablo Castro on 12/3/13.
//  Copyright (c) 2013 witty. All rights reserved.
//

#import "DrinkListViewController.h"

@interface DrinkListViewController () < UITextFieldDelegate,
                                        UICollectionViewDataSource,
                                        UICollectionViewDelegateFlowLayout>

@property(nonatomic, strong) NSMutableArray * drinkList;
@property (strong, nonatomic) IBOutlet UICollectionView *DrinksMenu;

@end

@implementation DrinkListViewController

- (void)viewDidLoad
{
    [super viewDidLoad];
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark - UICollectionView Datasource


- (NSInteger)collectionView:(UICollectionView *)view numberOfItemsInSection:(NSInteger)section {
//    NSString *searchTerm = self.searches[section];
//    return [self.searchResults[searchTerm] count];
    
    return 20;
    
}

- (NSInteger)numberOfSectionsInCollectionView: (UICollectionView *)collectionView {
//    return [self.searches count];

    return 2;
}

- (UICollectionViewCell *)collectionView:(UICollectionView *)cv
                  cellForItemAtIndexPath:(NSIndexPath *)indexPath {
    
    UICollectionViewCell *cell = [cv dequeueReusableCellWithReuseIdentifier:@"DrinkCell"
                                                               forIndexPath:indexPath];
    cell.backgroundColor = [UIColor whiteColor];
    return cell;
}


//- (UICollectionReusableView *)collectionView:
// (UICollectionView *)collectionView viewForSupplementaryElementOfKind:(NSString *)kind atIndexPath:(NSIndexPath *)indexPath
// {
// return [[UICollectionReusableView alloc] init];
//}


#pragma mark - UICollectionViewDelegate

- (void)collectionView:(UICollectionView *)collectionView didSelectItemAtIndexPath:(NSIndexPath *)indexPath
{
    // TODO: Select Item
}

- (void)collectionView:(UICollectionView *)collectionView didDeselectItemAtIndexPath:(NSIndexPath *)indexPath {
    // TODO: Deselect item
}















@end
