function draw_csl_balance_bar()
    dataset_0 = csvread('./data/cross-site-linking/user_attr_0.csv', 1, 2);
    dataset_1 = csvread('./data/cross-site-linking/user_attr_1.csv', 1, 2);
    dataset_2 = csvread('./data/cross-site-linking/user_attr_2.csv', 1, 2);
    dataset_3 = csvread('./data/cross-site-linking/user_attr_3.csv', 1, 2);
    
    num_0 = nnz(dataset_0(:,4) >= 0.5 & dataset_0(:,4) <= 2);
    num_1 = nnz(dataset_1(:,4) >= 0.5 & dataset_1(:,4) <= 2);
    num_2 = nnz(dataset_2(:,4) >= 0.5 & dataset_2(:,4) <= 2);
    num_3 = nnz(dataset_3(:,4) >= 0.5 & dataset_3(:,4) <= 2);
    
    Y = [num_0/length(dataset_0(:,4)) num_1/length(dataset_1(:,4)) num_2/length(dataset_2(:,4)) num_3/length(dataset_3(:,4))];
    X = {'Neither', 'TW only', 'FB only', 'Both'};
    bar(Y, 0.6, 'k');
    xlim([0.5 4.5]);
    set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
    set(gca, 'xticklabel', X);
    set(gca, 'FontSize', 12);
    xlabel('','FontSize',20);
    ylabel('Percentage(%)','FontSize',20);
    title('');
    grid off;
    print('./results/csl/csl_balance_bar.eps', '-depsc')
end